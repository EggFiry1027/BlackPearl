# -- coding: utf-8 --
# ba_meta require api 6
import ba,_ba,setting,os,json
from datetime import datetime


class PlayersLogger(object):
	"""An object which manages the players playing in the server"""
	def __init__(self):
		self.pData_path = os.path.join(_ba.env()['python_directory_user'],"playersData" + os.sep)
		if not os.path.exists(self.pData_path): os.makedirs(self.pData_path)
		self.players_file = self.pData_path + 'players.json'
		self.old_players = {}
		self.check_timer = ba.Timer(0.1, self.check, timetype=ba.TimeType.REAL, repeat=True)

	def get_pf(self):
		with open(self.players_file, encoding="utf-8") as f:
			return json.loads(f.read())

	def dump_pf(self, d: dict):
		with open(self.players_file, "w") as f:
			json.dump(d, f, indent=4)

	def check(self):
		time = int(ba.time(timetype=ba.TimeType.REAL, timeformat=ba.TimeFormat.MILLISECONDS))
		lptime = 'Last Played at - ' + str(datetime.now())
		pf = self.get_pf()
		players = {}

		#Update self.players and their activity in players.json
		for i in _ba.get_game_roster():

			#check if we have got account_id
			if i['account_id'] and (i['account_id'].startswith('pb-')) and (i['client_id'] != -1):
				aid = i['account_id']
				ds = i['display_string']
				cid = i['client_id']

				#add them to our players
				players[aid] = ds

				#update their details in players.json
				if aid not in pf: pf[aid] = {'aid': aid, 'devices': [ds], 'status': 'playing'}
				else:
					pf[aid]['status'] = 'playing'
					if ds not in pf[aid]['devices']: pf[aid]['devices'].append(ds)

		#Check for player leavings..
		if self.old_players:
			for uID,name in self.old_players.items():

				#Check if someone left 
				if uID not in players:

					#Update the leaving time in their status
					if uID in pf: pf[uID]['status'] = lptime

		self.dump_pf(pf)
		self.old_players = players

# ba_meta export plugin
class start_logging(ba.Plugin):
	def on_app_launch(self):
		PlayersLogger()