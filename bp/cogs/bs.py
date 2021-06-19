from bp.storage import *
import discord, random, os, json, shutil
from discord import DMChannel
from discord.ext import commands
from datetime import datetime
from bp.mycloud import SFTP
from bp.livestats import LiveStats

def get_stats_file_from_local(s: str):
	p = bs_servers_path + s + step + 'data' + step + 'stats.json'
	if os.path.exists(p):
		with open(p, encoding="utf-8") as d:
			a = json.loads(d.read())
			d.close()
			return a
def get_players_file_from_local(s: str):
	p = bs_servers_path + s + step + 'data' + step + 'players.json'
	if os.path.exists(p):
		with open(p, encoding="utf-8") as d:
			a = json.loads(d.read())
			d.close()
			return a

class BombSquad(commands.Cog):
	"""docstring for BombSquad"""
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("BombSquad Cog Running.")

	@commands.command()
	async def stats(self, ctx, pc: str = None, player: str = None):
		eeeeee = 'ee'
		async def send_not_found(sn: str):
			await ctx.reply(f"Player **`{player}`** not found in **`{sn}`**")
		async def send_stats(sn: str, s: dict, pd: dict):
			t = s['name']
			d = f'\n\n***Stats from `{sn}`***\n'
			if pd != {} and 'devices' in pd:
				d += f"**Devices:**\n*```{pd['devices']}```*\n"
			emd = myembed(title=t, description=d, color=get_embed_color())
			for k,v in s.items():
				if k not in ['name', 'name_html', 'aid']:
					emd.add_field(name=f'***`{k}`***', value=f'**`{v}`**')
			emd.set_footer(text=f"{s['aid']}")
			await ctx.reply(embed=emd)
		async def process_stats_Req(sn: str, sts: dict, pys: dict):
			p_stats = {}
			p_details = {}
			if player.startswith('pb-'):
				if player in sts: p_stats = sts[player]
				if player in pys: p_details = pys[player]
			else:
				asp = [(a['name'], a['aid']) for a in sts.values()]
				for sp in asp:
					if (player == sp[0][1:]) or (player in sp[0]): p_stats = sts[sp[1]]
				if pys != {}:
					adp = [(a['devices'], a['aid']) for a in pys.values()]
					for dp in adp:
						if player in dp[0]:
							p_details = pys[dp[1]]
							break
						for d in dp[0]:
							if (player == d) or (player in d):
								p_details = pys[dp[1]]
								break
			if (p_details == {}) and (p_stats == {}): await send_not_found(sn)
			else: await send_stats(sn, p_stats, p_details)
		if (player == None) or (player in dc_names):
			await ctx.reply(f"***Usage:***\n**```{ctx.prefix}stats <party_code> <PC-ID/Andro-ID/Google-ID/display_str/account_id>```**")
			return
		servers = get_json('bs_servers')
		if pc not in servers:
			await ctx.reply(f"The `party_code` **`{pc}`** is wrong or doesn't exists!")
			return
		else:
			pn = LiveStats().get_ls(pc)['party_name']
			stats = get_stats_file_from_local(pc)
			players_data = {}
			if 'players' in servers[pc]:
				players_data = get_players_file_from_local(pc)
			await process_stats_Req(pn, stats, players_data)
			return

	@commands.command()
	async def top(self, ctx, p: str = None, discrim: str = None, limit: int = 15):
		eea = 'e'
		dc_names = {
		'score': ['scores', 'Score'],
		'avg_score': ['avg_score', 'Average Score'],
		'games': ['games', "Games Played"],
		'kills': ['kills', 'Total Kills'],
		'deaths': ['deaths', 'Total Deaths'],
		'kd': ['kd', 'Kill/Death Ratio'],
		'damage': ['total_damage', 'Damage Dealt']
		}
		async def send_top(sn: str, toppers: list, s: dict, dcr: str):
			t = f"*Toppers of  -  `{sn}`*"
			d = u"**```\n{0:^4} - {1:^15} - {2:^8}\n".format('Rank', 'Player Name', dc_names[dcr][1])
			i = 1
			for tpr in toppers:
				if i < limit:
					d += u"{0:^4} - {1:^15} - {2:^8}\n".format(str(i), s[tpr[1]]['name'], str(s[tpr[1]][dc_names[dcr][0]]))
					i += 1
			d += '```**'
			emd = myembed(title=t, description=d, color=get_embed_color())
			await ctx.send(embed=emd)
		async def send_cmd():
			await ctx.reply(f"***Usage:***\n**```{ctx.prefix}top <party_code> [Discrimination] [Max Limit]```**\n**Available Keys for Optional Args:**\n**`Discrimination`:** *`score [default], avg_score, games, kills, deaths, kd, damage`*\n**`Max Limit`:** *`int() < 20`*")
		if (p == None) or (not isinstance(limit, int)) or (limit > 20) or discrim not in dc_names:
			await send_cmd()
			return
		servers = get_json('bs_servers')
		if p not in servers:
			await ctx.reply(f"The `party_code` **`{p}`** is wrong or doesn't exists!")
			return
		pn = LiveStats().get_ls(p)['party_name']
		stats = get_stats_file_from_local(p)
		if 'players' in servers[p]:
			players_data = get_players_file_from_local(p)
		if discrim == None:
			all_players = [(a['scores'], a['aid']) for a in stats.values()]
			all_players.sort(reverse=True)
			await send_top(pn, all_players, stats, "score")
			return
		else:
			all_players = [(a[dc_names[discrim][0]], a['aid']) for a in stats.values()]
			all_players.sort(reverse=True)
			await send_top(pn, all_players, stats, discrim)
			return

def setup(bot):
	bot.add_cog(BombSquad(bot))