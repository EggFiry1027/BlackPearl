import discord, os, json
from bp import mycloud, livestats
from discord import DMChannel as dm
from bp.storage import *

msg_p = {}
msg_cp = {}
msg_cpc = {}
confirm_asked = False

class Msg(object):
	"""docstring for Msg"""
	def __init__(self):
		self.next_qn = {
			'build': "Do you **use BCS** (BombSquad Consultancy Services) build, [https://github.com/imayushsaini/Bombsquad-Ballistica-Modded-Server] **?**\n**`Note:`** (1) If you have **not** changed/renamed anything (folders/files) in BCS build: send `bcs`\n\t(2) If you **have changed/renamed** any folders: send `renamed`\n\t(3) If you use anyother script/build: send `custom`",
			'key': "***Now we are in Last Step***:\n**Send only** the private access key ***`.pem`*** file of that server as an attachment...\n**Note: This can't be reset**"
		}
		self.bcs = {
		'ls': bcs_mods_path + 'stats/ls.json',
		'stats': bcs_mods_path + 'stats/stats.json',
		}

	def set_process(self, user: int, process: str, status: dict, bot):
		msg_p[user] = process
		msg_cp[user] = status
		self.bot = bot
		msg_cpc[user] = {
			'k': 'ip',
			'v': None,
			'next_qn': self.next_qn['build'],
			'next_process': 'pa_build',
			'current_qn': ip_qn,
			'sending_mods_path': False
			}

	async def handle_msg(self, m: discord.Message, bot):
		global msg_p
		global msg_cp
		global msg_cpc
		self.bot = bot
		u = m.author
		if (not u.bot) and (u.id in msg_p) and (msg_p[u.id].startswith('pa')):
			await self.handle_party_add(u, m)
		return False

	async def handle_party_add(self, u, m):

		if hasattr(m.channel, 'guild'): return
		msg = m.content.lower()
		uid = u.id
		sn = msg_cp[uid]['server_name']

		async def ask(user, qn):
			try: await dm.send(user, qn)
			except: pass

		async def ask_confirm():
			await ask(u, "**Are you Sure?**, say `yes` or `no`...")

		async def cancel():
			if uid in msg_cp:
				if 'key' in msg_cp[uid]['server_details']:
					k = msg_cp[uid]['server_details']['key']
					os.remove(k)
					os.rmdir(os.getcwd() + bs_servers_path[1:] + sn + step)
				msg_cp.pop(uid)
			msg_p.pop(uid)
			msg_cpc.pop(uid)
			await ask(u, "Party adding Process has been Successfully Cancelled!")

		async def add_server():
			chnl = await self.bot.get_channel(msg_cp[uid]['server_details']['chnl'])
			ouremd = myembed(
				title=sn,
				description="Setting up the server and adding live stats plugin..."
				)
			lives_stats.server_embeds[sn] = await chnl.send(embed=ouremd)
			await livestats.LiveStats().add_server(msg_cp[uid]['server_name'], msg_cp[uid]['server_details'])
			msg_cpc.pop(uid)
			msg_cp.pop(uid)
			msg_p.pop(uid)

		#Calcel Anytime
		if msg.startswith('cancel'):
			await ask(u, "Ok I am Cancelling the process...")
			await cancel()
			return

		#Check Confirmation
		if uid in msg_cpc:
			if (msg_cpc[uid]['k'] == 'build'):
				if msg.startswith('bcs'):
					msg_cp[uid]['server_details']['mods'] = bcs_mods_path
					msg_cp[uid]['server_details']['ls'] = self.bcs['ls']
					msg_cp[uid]['server_details']['stats'] = self.bcs['stats']
					msg_p[uid] = msg_cpc[uid]['next_process']
					await ask(u, msg_cpc[uid]['next_qn'])
				elif msg.startswith('renamed') and (msg not in (None, '')):
					msg_cpc[uid]['sending_mods_path'] = True
					await ask(u, f"Ok, Now send the edited **`mods folder path`**\nThe BCS's default mods path will be ***`{bcs_mods_path}`***")
					return
				elif msg.startswith('custom'):
					await ask(u, "Cancelling process..., This Bot Supports Only BCS Build For now!")
					await cancel()
					return
				else:
					if msg_cpc[uid]['sending_mods_path'] == True:
						msg_cp[uid]['server_details']['mods'] = msg
						msg_cp[uid]['server_details']['ls'] = msg + '/stats/ls.json'
						msg_cp[uid]['server_details']['stats'] = msg + '/stats/stats.json'
						msg_p[uid] = msg_cpc[uid]['next_process']
						await ask(u, msg_cpc[uid]['next_qn'])
			if msg.startswith('yes') and confirm_asked:
				if msg_cpc[uid]['k'] != 'build':
					msg_p[uid] = msg_cpc[uid]['next_process']
					msg_cp[uid]['server_details'][msg_cpc[uid]['k']] = msg_cpc[uid]['v']
				await ask(u, msg_cpc[uid]['next_qn'])
				confirm_asked = False
			if msg.startswith('no') and confirm_asked:
				if msg_cpc[uid]['k'] == 'build':
					await ask(u, "Considering the reply as a negative one, as the bot only supports BCS Script - **Cancelling Process**")
					await cancel()
					confirm_asked = False
					return
				else:
					await ask(u, "***This time be careful,***\n" + msg_cpc[uid]['current_qn'])
					confirm_asked = False
					return

		###################### The Answers/Values handling #######################

		if msg_p[uid] == 'pa_ip' and (uid in msg_cp):
			if (not m.content == None) and (not m.content == ''):
				u_ip = m.content.strip(' abcdefghijklmnoprstuvwqxyz')
				try:
					if len(u_ip.split('.')) == 4:
						try:
							u_ip = float(u_ip)
							u_ip = str(u_ip)
						except:
							u_ip = str(u_ip)
					else:
						await ask(u, "Invalid IP Adress, Send Correct one :/")
						return
				except:
					await ask(u, "Invalid IP Adress, Send Correct one :/")
					return
				msg_cpc[uid] = {
					'k': 'ip',
					'v':u_ip,
					'next_qn': self.next_qn['build'],
					'next_process': 'pa_build',
					'current_qn': ip_qn,
					'sending_mods_path': False
					}
				await ask_confirm()
				confirm_asked = True
				return
			else:
				await ask(u, "Nob, What have you sent, **read carefuly again**...\n" + ip_qn)
				return

		if (msg_p[uid] == 'pa_build') and (uid in msg_cp):
			if (not m.content == None) and (not m.content == ''):
				msg_cpc[uid] = {
					'k': 'build',
					'v': m.content,
					'next_qn': self.next_qn['key'],
					'next_process': 'pa_key',
					'current_qn': self.next_qn['build'],
					'sending_mods_path': False
					}
				return
			else:
				await ask(u, "Nob, What have you sent, **read carefuly again**...\n" + self.next_qn['build'])
				return

		if (msg_p[uid] == 'pa_key') and (uid in msg_cp):
			atchs = m.attachments
			if (atchs != []) and (atchs is not None):
				k = atchs[0]
				if not k.filename.endswith('.pem'):
					await ask(u, "Nob, What have you sent, **I asked `.pem` file**, Send The correct one again...")
					return
				folder = os.getcwd() + bs_servers_path[1:] + sn + step
				if not os.path.exists(folder): os.mkdir(folder)
				file = folder +  k.filename
				await k.save(file)
				msg_cp[uid]['server_details']['key'] = file
				if not sn == 'test':
					await add_server()
					return
				else:
					await ask(u, "Testing Done...")
					msg_p.pop(uid)
					msg_cp.pop(uid)
					msg_cpc.pop(uid)
					return