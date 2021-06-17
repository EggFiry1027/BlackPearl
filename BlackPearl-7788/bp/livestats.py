from bp.storage import *
from bp.cloud import SFTP
import os, json, pytz, random
from datetime import datetime
from bp.blackPearl import bot
import urllib.request as web

server_embeds = {}
#
def get_clean_bs_name(name):
	n = name
	newname = list(n)
	nme = ''
	ee = {
	'': ' <:bs_googleplay:854727544032329788>',
	'': ' <:bs_knight:854727645358587934>',
	'': ' <:bs_local:854727737713098763>',
	'': ' <:bs_bomb:854727832860491867>',
	'': ' <:bs_moon:854727943574257714>',
	'': ' <:bs_crown:854728340329201714>',
	'': ' <:bs_logo:854728380900442122>',
	'': ' <:bs_heart:854728425905061908>',
	'': ' <:bs_skull:854728475625914368>',
	'': ' <:bs_gamecenter:854728723583991859>',
	'': ' <:bs_gamecircle:854728774645579857>',
	'': ' <:bs_meteorite:854728817498259487>',
	'': ' <:bs_spider:854728891007631360>',
	'': ' <:bs_pheonix:854728999367344148>',
	'': ' <:bs_ninjastar:854729061095964712>',
	'': ' <:bs_mushroom:854729256756445215>',
	'': ' <:bs_eye:854729307061747735>',
	'': ' <:bs_hat:854729360821321748>',
	'': ' <:bs_viking:854729759237341194>',
	'': ' <:bs_yinyang:854727433635102751>',
	'\\n': '',
	'\n': '',
	'`': '',
	'*': ''
	}
	if (len(n) > 10): n = n[:10] + '...'
	for k, v in ee.items():
		if k in n:
			if k == '':
				if n[1:].startswith('Server'):
					newname.insert(0, ' <:bs_gather:854728292606804028> ')
					newname.remove(k)
				else:
					newname.insert(0, v)
					newname.remove(k)
			else:
				newname.insert(0, v)
				newname.remove(k)
	return nme.join(newname)

class LiveStats(object):
	'''
	#An Example for SFTP
	import os, paramiko

	server_file = '/root/ak/players.json'
	my_file = 'players.json'
	ip = '147.139.28.63'
	un = 'root'
	kf = f'.{os.sep}Test.pem'

	k = paramiko.RSAKey.from_private_key_file(kf)
	c = paramiko.SSHClient()
	c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print("connecting") 
	c.connect(hostname=ip, username=un, pkey=k)
	print("connected")
	sftp = c.open_sftp()
	sftp.get(server_file, my_file)
	sftp.close()
	c.close()
	print('success')

	'''
	def __init__(self):
		self.e = 'e'

	async def add_server(self, sn: str, sd: dict):
		try:
			servers = get_json('bs_servers')
			servers[sn] = sd
			dump_json('bs_servers', servers)
			#Put Plugin
			plugin = bdata + 'lives_stats_plugin.json'
			c = SFTP().connect(sd['ip'], 'ubuntu', sd['key'])
			sftp = c.open_sftp()
			sftp.put(plugin, sd['mods'])
			sftp.close()
			c.close()
		except Exception as e:
			emd = myembed(title=sn, description=f"```Error:\n{e}```")
			await server_embeds[sn].edit(embed = myembed)

	def get_ls(self, s: str):
		p = bs_servers_path + s + step + 'data' + step + 'ls.json'
		with open(p, encoding="utf-8") as d:
			a = json.loads(d.read())
			d.close()
			return a

	async def update_live(self):
		servers = get_json('bs_servers')
		if servers == {}: return
		for svr in servers:

			#Update ls.json (live_stats) Files
			s = servers[svr]
			SFTP().get_file(svr, 'ls')

			#Get the Data
			ls = {}
			try: ls = self.get_ls(svr)
			except: continue

			#title
			all_owners = s['dc_owners']
			owner_name = ""
			for onr in all_owners:
				if isinstance(onr, str):
					owner_name = onr
					break
				if isinstance(onr, int):
					owner_name = await get_dc_user_name(bot, onr)
					break
			if 'web' in s: pn = f"[{ls['party_name']}]({s['web']})"
			else: pn = ls['party_name']
			livep = ls['livep']
			maxp = ls['maxp']
			title = f'*`{pn}`*'

			#description
			description = f'\n\t\n**Players in Party:** (**`{str(livep)}`/`{str(maxp)}`**)\n**Party Code: `{svr}`**\n'
			#players
			plist = f'\n***Live Stats***\n'
			ros = ls['roster']
			for i in ros:
				if i['account_id'] != None:
					lnk = 'http://bombsquadgame.com/accountquery?id=' + i['account_id']
					PD = f"[Info]({lnk})"
				else:
					PD = f"`No Info`"
				ds = get_clean_bs_name(i['display_string'])
				if i['players'] == [] or not i['players']:
					plist += f'{ds} - <:bs_gather:854728292606804028>`In Lobby` - {PD}\n'
				else:
					for p in i['players']:
						pds = get_clean_bs_name(p['name_full'])
						plist += f'{ds} - {pds} - {PD}\n'
			#chats
			chats = '***LiveChats***\n```'
			chat_index = 1
			for c in ls['chats']:
				if chat_index <= 13:
					if '`' in c: c.replace('`', '')
					chats += f'{c}\n'
					chat_index += 1
			#Time
			tz = pytz.timezone('Asia/Kolkata')
			timenow = datetime.now(tz)
			ct = timenow.strftime('%I:%M:%S%p-%d/%b/%Y')
			description += f"{plist}\n{chats}```-----------------------------------\n{ct} :P"

			#EMBED
			emd = myembed(title=title, description=description, color=get_embed_color())
			bs_icon = 'https://play-lh.googleusercontent.com/CachTgIoVy7oEtLlgeo8bPcJfaUHRopRYUOH-DYyeiRsQQaqg8gjpp1qGgOs3wiC2IQ'
			emd.set_author(name=owner_name, icon_url=bs_icon)

			#Update Discord Chat
			if len(str(emd.description)) < 1999:
				try:
					if svr in server_embeds:
						try: await server_embeds[svr].edit(embed=emd)
						except: pass
					else:
						try: chnl = bot.get_channel(s['chnl'])
						except Exception as err:
							print(err)
							return
						if chnl is not None:
							try:
								m = await chnl.send(embed=emd)
								server_embeds[svr] = m
							except: pass
				except:
					try: chnl = bot.get_channel(s['chnl'])
					except Exception as err:
						print(err)
						return
					if chnl is not None:
						try:
							m = await chnl.send(embed=emd)
							server_embeds[svr] = m
						except: pass