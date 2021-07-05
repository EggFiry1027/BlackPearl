import discord, os, json, random
from discord.ext import commands
from datetime import datetime
import urllib.request as web

#Global Variables
bcs_mods_path = '/home/ubuntu/Bombsquad-Ballistica-Modded-Server/dist/ba_root/mods/'
myembed = discord.Embed
step = str(os.sep)
mydir = str(os.getcwd() + step + 'bp' + step)
bdata = f'{mydir}bdata{step}'
bs_servers_path = f'{mydir}bs_servers{step}'
temp_folder = f'{mydir}temp{step}'
clr = discord.Color
msg_p = {}
msg_cp = {}
msg_cpc = {}
dc_names = {
	'score': ['scores', 'Score'],
	'avg_score': ['avg_score', 'Average Score'],
	'games': ['games', "Games Played"],
	'kills': ['kills', 'Total Kills'],
	'deaths': ['deaths', 'Total Deaths'],
	'kd': ['kd', 'Kill/Death Ratio'],
	'damage': ['total_damage', 'Damage Dealt']
	}
colors = {
	"red": clr.red(),
	"blue": clr.blue(),
	"green": clr.green()
	}

files = {
	'bot': f'{bdata}data.json',
	'guilds': f'{bdata}guilds.json',
	'bs_servers': f'{bdata}bs_servers.json'
	}
server_embeds = {}
ip_qn = "Now you are in process of adding a livestats server, Now send the ***`Internet Protocot Adress`/`IP Adress`*** of your web/cloud server in which a BombSquad 1.6 Server Build is running...\n**`Example:`** 192.168.43.1...\n***You can Cancel the process anytime before the submission by sending `cancel`***\nIf you **don't use AWS**, `cancel` the process :("

def get_clean_user_id(u: str):
	ID = str(u)
	ID = ID.split('<@!')[1]
	ID = ID.split('>')[0]
	return int(ID)

def get_clean_guild_name(g: str):
	invalid = ['|', '/', '\\', '(', ')', '{', '}', '[', ']', '<', '>', ',', "'", '"', '#', '!', '@', '$', '%', '^', '&', '*' , '=', '+']
	name = g
	e = list(name)
	new_name = ""
	for i in invalid:
		if i in name:
			p = e.index(i)
			e.index(p, '')
			e.remove(i)
	return new_name.join(e)

async def get_dc_user_name(bot, user_id):
	u = await bot.fetch_user(user_id)
	return u.name + '#' + u.discriminator

def get_rc():
	return random.randint(0, 200)

def get_embed_color():
	c = discord.Color.from_rgb(get_rc(), get_rc(), get_rc())
	return c

def get_json(f: str):
	try:
		if f in files:fn = files[f]
		else: fn = f
		with open(fn, encoding="utf-8") as d:
			a = json.loads(d.read())
			d.close()
			return a
	except Exception as e: print(e)

def dump_json(f: str, d: dict, temp=False):
	try:
		if not temp:
			if f in files:
				ff = open(files[f], 'w')
				ff.write(json.dumps(d, indent=4))
				ff.close()
				if f != 'bs_servers': print(f"Data Updated: '{f}.json' has been updated! || {datetime.now()}")
			else: print(f"File not found in bot's file variable")
		else:
			ff = open(f, 'w')
			ff.write(json.dumps(d, indent=4))
			ff.close()
	except Exception as e: print(e)

def check_server_perms(u: int):
	users = get_json('bot')
	if (int(u) in users['owners']) or (int(u) in users['server_owners']): return True
	return False

def check_top_cmd_perms(u: int):
	users = get_json('bot')
	if (int(u) in users['owners']) or (int(u) in users['admins']) or (int(u) in users['server_owners']): return True
	return False

def check_owner_perms(u: int):
	users = get_json('bot')['owners']
	if int(u) in users: return True
	return False

def get_response(url):
	req = web.Request(url)
	with web.urlopen(req) as response:
		r = response.read()
		if isinstance(r, dict): return json.loads(r)
		else: return r

for f in files:
	j = files[f]
	if not os.path.exists(j):
		dump_json(f, {})