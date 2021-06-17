import discord, os, json, paramiko
from bp.storage import *
from datetime import datetime

class SFTP(object):
	def __init__(self):
		self.servers = get_json('bs_servers')

	def connect(self, ip: str, un: str, pem: str):
		k = paramiko.RSAKey.from_private_key_file(pem)
		c = paramiko.SSHClient()
		c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		c.connect(hostname=ip, username=un, pkey=k)
		return c

	def get_dir_list(self, path: str):
		dirlist = []
		if os.path.isdir(path):
			try: dirlist = os.listdir(path)
			except Exception as e:
				import errno
				if (type(e) == OSError
						and e.errno in (errno.EACCES, errno.ENOENT)):
					pass # we expect these sometimes..
				else: print(e)
		return dirlist

	def has_key(self, server: str):
		if server in self.servers:
			s = self.servers[server]
			if os.path.exists(s['key']):
				return True
			else:
				return False
		return False

	def get_file(self, server: str, file: str):
		if not self.has_key(server):
			print(f"We don't have required access files/data for '{server}' to get '{file}' from there!")
			return
		try:
			self.servers = get_json('bs_servers')
			s = self.servers[server]

			#If no Folder for the server is exists, create one!
			local_folder = f'{mydir}bs_servers/{server}/data/'
			if not os.path.exists(local_folder): os.mkdir(local_folder)
			local_file = f'{local_folder}{file}.json'
			#and for the file too
			if not os.path.exists(local_file):
				f = open(local_file, 'w')
				f.write('{}')
				f.close()

			if file in s:
				server_file = s[file]
				c = self.connect(s['ip'], 'ubuntu', s['key'])
				sftp = c.open_sftp()
				sftp.get(server_file, local_file)
				sftp.close()
				c.close()
			else: print(f'\'{file}\' not found in {server}')
		except Exception as e: print(e)

	def upload_file(self, server: str, file: str):
		print('sftp upload disabled!')
		return

	def update_stats(self):
		self.servers = get_json('bs_servers')
		for s in self.servers:
			get_file(s, 'stats')

	def update_players(self):
		print('cloud: players.json disabled')
		return
		for s in self.servers:
			get_file(s, 'players')
SFTP()