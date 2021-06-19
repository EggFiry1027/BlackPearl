from bp.storage import *
import discord, os, json
from discord import DMChannel as dm

class Msg(object):
	"""docstring for Msg"""
	def __init__(self):
		self.msg_p = {}
		self.msg_cp = {}
		self.msg_cpc = {}
		self.next_qn = {
			'build': "Do you **use BCS** (BombSquad Consultancy Services) build, [https://github.com/imayushsaini/Bombsquad-Ballistica-Modded-Server] **?**\n**`Note:`** (1) If you have **not** changed/renamed anything (folders/files) in BCS build: send `bcs`\n\t(2) If you **have changed/renamed** any folders: send `renamed`\n\t(3) If you use anyother script/build: send `custom`",
			'key': "***Now we are in Last Step***:\n**Send only** the private access key ***`.pem`*** file of that server as an attachment...\n**Note: This can't be reset**"
		}
		self.bcs = {
		'ls': bcs_mods_path + 'stats/ls.json',
		'stats': bcs_mods_path + 'stats/stats.json',
		}

	def set_process(self, user: int, process: str, status: dict, bot):
		self.msg_p[user] = process
		self.msg_cp[user] = status
		self.bot = bot
		self.msg_cpc[user] = {
			'k': 'ip',
			'v': None,
			'next_qn': self.next_qn['build'],
			'next_process': 'pa_build',
			'current_qn': ip_qn,
			'sending_mods_path': False,
			'confirm_asked': False
			}

	async def handle_msg(self, m: discord.Message, bot):
		self.bot = bot
		u = m.author
		if (not u.bot) and (u.id in msg_p) and (msg_p[u.id].startswith('pa')):
			await self.handle_party_add(u, m)
		return False

	async def handle_party_add(self, u, m):

		if hasattr(m.channel, 'guild'): return
		msg = m.content.lower()
		uid = u.id
		sn = self.msg_cp[uid]['server_name']

		async def ask(user, qn):
			try: await dm.send(user, qn)
			except: pass

		async def ask_confirm():
			await ask(u, "**Are you Sure?**, say `yes` or `no`...")

		async def cancel():
			if uid in self.msg_cp:
				if 'key' in self.msg_cp[uid]['server_details']:
					k = self.msg_cp[uid]['server_details']['key']
					os.remove(k)
					os.rmdir(os.getcwd() + bs_servers_path[1:] + sn + step)
				self.msg_cp.pop(uid)
			self.msg_p.pop(uid)
			self.msg_cpc.pop(uid)
			await ask(u, "Party adding Process has been Successfully Cancelled!")

		async def add_server():
			chnl = await self.bot.get_channel(self.msg_cp[uid]['server_details']['chnl'])
			ouremd = myembed(
				title=sn,
				description="Setting up the server and adding live stats plugin..."
				)
			from bp.livestats import LiveStats, server_embeds
			server_embeds[sn] = await chnl.send(embed=ouremd)
			await LiveStats().add_server(self.msg_cp[uid]['server_name'], self.msg_cp[uid]['server_details'])
			self.msg_cpc.pop(uid)
			self.msg_cp.pop(uid)
			self.msg_p.pop(uid)

		#Calcel Anytime
		if msg.startswith('cancel'):
			await ask(u, "Ok I am Cancelling the process...")
			await cancel()
			return

		#Check Confirmation
		if uid in self.msg_cpc:
			if (self.msg_cpc[uid]['k'] == 'build'):
				if msg.startswith('bcs'):
					self.msg_cp[uid]['server_details']['mods'] = bcs_mods_path
					self.msg_cp[uid]['server_details']['ls'] = self.bcs['ls']
					self.msg_cp[uid]['server_details']['stats'] = self.bcs['stats']
					self.msg_p[uid] = self.msg_cpc[uid]['next_process']
					await ask(u, self.msg_cpc[uid]['next_qn'])
				elif msg.startswith('renamed') and (msg not in (None, '')):
					self.msg_cpc[uid]['sending_mods_path'] = True
					await ask(u, f"Ok, Now send the edited **`mods folder path`**\nThe BCS's default mods path will be ***`{bcs_mods_path}`***")
					return
				elif msg.startswith('custom'):
					await ask(u, "Cancelling process..., This Bot Supports Only BCS Build For now!")
					await cancel()
					return
				else:
					if self.msg_cpc[uid]['sending_mods_path'] == True:
						self.msg_cp[uid]['server_details']['mods'] = msg
						self.msg_cp[uid]['server_details']['ls'] = msg + '/stats/ls.json'
						self.msg_cp[uid]['server_details']['stats'] = msg + '/stats/stats.json'
						self.msg_p[uid] = self.msg_cpc[uid]['next_process']
						await ask(u, self.msg_cpc[uid]['next_qn'])
			if msg.startswith('yes') and self.msg_cpc[uid]['confirm_asked'] == True:
				if self.msg_cpc[uid]['k'] != 'build':
					self.msg_p[uid] = self.msg_cpc[uid]['next_process']
					self.msg_cp[uid]['server_details'][self.msg_cpc[uid]['k']] = self.msg_cpc[uid]['v']
				await ask(u, self.msg_cpc[uid]['next_qn'])
				self.msg_cpc[uid]['confirm_asked'] = False
			if msg.startswith('no') and self.msg_cpc[uid]['confirm_asked'] == True:
				if self.msg_cpc[uid]['k'] == 'build':
					await ask(u, "Considering the reply as a negative one, as the bot only supports BCS Script - **Cancelling Process**")
					await cancel()
					self.msg_cpc[uid]['confirm_asked'] = False
					return
				else:
					await ask(u, "***This time be careful,***\n" + self.msg_cpc[uid]['current_qn'])
					self.msg_cpc[uid]['confirm_asked'] = False
					return

		###################### The Answers/Values handling #######################

		if self.msg_p[uid] == 'pa_ip' and (uid in self.msg_cp):
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
				self.msg_cpc[uid] = {
					'k': 'ip',
					'v':u_ip,
					'next_qn': self.next_qn['build'],
					'next_process': 'pa_build',
					'current_qn': ip_qn,
					'sending_mods_path': False
					}
				await ask_confirm()
				self.msg_cpc[uid]['confirm_asked'] = True
				return
			else:
				await ask(u, "Nob, What have you sent, **read carefuly again**...\n" + ip_qn)
				return

		if (self.msg_p[uid] == 'pa_build') and (uid in self.msg_cp):
			if (not m.content == None) and (not m.content == ''):
				self.msg_cpc[uid] = {
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

		if (self.msg_p[uid] == 'pa_key') and (uid in self.msg_cp):
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
				self.msg_cp[uid]['server_details']['key'] = file
				if not sn == 'test':
					await add_server()
					return
				else:
					await ask(u, "Testing Done...")
					self.msg_p.pop(uid)
					self.msg_cp.pop(uid)
					self.msg_cpc.pop(uid)
					return
Msg()