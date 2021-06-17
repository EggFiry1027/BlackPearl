from bp.storage import *
import discord, random, os, json, shutil
from discord import DMChannel
from discord.ext import commands
from datetime import datetime
from bp.cloud import SFTP
from bp.livestats import LiveStats

def get_stats_file_from_local(s: str):
	p = bs_servers_path + s + step + 'data' + step + 'stats.json'
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
		async def send_stats(sn: str, s: dict):
			t = s['name']
			d = f'\n\n***Stats from `{sn}`***'
			emd = myembed(title=t, description=d, color=get_embed_color())
			for k,v in s.items():
				if k not in ['name', 'name_html', 'aid']:
					emd.add_field(name=f'***`{k}`***', value=f'**`{v}`**')
			emd.set_footer(text=f"{s['aid']}")
			await ctx.reply(embed=emd)
		async def send_not_found(sn: str):
			await ctx.reply(f"Player **`{player}`** not found in **`{sn}`**")
		if player == None:
			await ctx.reply(f"***Usage:***\n**```{ctx.prefix}stats <party_code> <player's name/display_str/account_id>```**")
			return
		servers = get_json('bs_servers')
		if pc not in servers:
			await ctx.reply(f"The `party_code` **`{pc}`** not Found!")
			return
		else:
			pn = LiveStats().get_ls(pc)['party_name']
			stats = get_stats_file_from_local(pc)
			if player.startswith('pb-'):
				if player in stats:
					await send_stats(pn, stats[player])
					return
				else:
					await send_not_found(pn)
					return
			all_players = [(a['name'], a['aid']) for a in stats.values()]
			for p in all_players:
				if p[0][1:] == player:
					await send_stats(pn, stats[p[1]])
					return
			await send_not_found(pn)
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
			emd = myembed(title=t, description=d)
			await ctx.send(embed=emd)
		async def send_cmd():
			await ctx.reply(f"***Usage:***\n**```{ctx.prefix}top <party_code> [Discrimination] [Max Limit]```**\n**Available Keys for Optional Args:**\n**`Discrimination`:** *`score [default], avg_score, games, kills, deaths, kd, damage`*\n**`Max Limit`:** *`int() < 20`*")
		if (p == None) or (not isinstance(limit, int)) or (limit > 20):
			await send_cmd()
			return
		servers = get_json('bs_servers')
		if p not in servers:
			ctx.reply(f"The `party_code` **`{p}`** not Found!")
			return
		pn = LiveStats().get_ls(p)['party_name']
		stats = get_stats_file_from_local(p)
		if discrim == None:
			all_players = [(a['scores'], a['aid']) for a in stats.values()]
			all_players.sort(reverse=True)
			await send_top(pn, all_players, stats, "score")
			return
		if discrim == 'kd':
			all_players = [(a[dc_names[discrim][0]], a['aid']) for a in stats.values()]
			all_players.sort()
			await send_top(pn, all_players, stats, 'kd')
			return
		else:
			all_players = [(a[dc_names[discrim][0]], a['aid']) for a in stats.values()]
			all_players.sort(reverse=True)
			await send_top(pn, all_players, stats, discrim)
			return

def setup(bot):
	bot.add_cog(BombSquad(bot))