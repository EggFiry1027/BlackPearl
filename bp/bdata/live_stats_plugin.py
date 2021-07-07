# -*- coding: utf-8 -*-
# ba_meta require api 6
import ba, _ba, os, json, yaml

class StartUpdating(object):
	"""docstring for start"""
	def __init__(self):
		self.timer = ba.Timer(1, self.update, timetype=ba.TimeType.REAL, repeat=True)

	def update(self):
		modspath = _ba.env()['python_directory_user']
		cfg = modspath.split('dist')[0] + 'config.yaml'
		party_name = ""
		with open(cfg, 'r') as stream:
			data_loaded = yaml.safe_load(stream)
		party_name = data_loaded['party_name']
		chats = _ba.get_chat_messages()
		if len(chats) > 15:
			chats = chats[-16:]
		ros = _ba.get_game_roster()
		ls = {
		'party_name': party_name,
		'livep': len(ros),
		'maxp': _ba.get_public_party_max_size(),
		'roster': ros,
		'chats': chats
		}
		folder = f'{modspath}/stats/'
		if not os.path.exists(folder): os.mkdirs(folder)
		file = folder + 'ls.json'
		f = open(file, 'w')
		f.write(json.dumps(ls, indent=2))
		f.close()

# ba_meta export plugin
class LivesStats(ba.Plugin):
	def on_app_launch(self):
		StartUpdating()