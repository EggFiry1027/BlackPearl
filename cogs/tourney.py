import discord, random, os
from BlackPearl.bp.storage import *
from discord.ext import commands
from datetime import datetime
rplayers = []

class Tournament(commands.Cog):
	"""docstring for BombSquad"""
	def __init__(self, bot):
		self.bot = bot

	#STATS
	@commands.command(aliases=['mm', 'match_make'])
	async def matchmake(self, ctx, Type=None, title=None, *, players=None):
		atypes = ('solo', 'duo', 'trio', 'squad')
		if (Type == None) or (Type not in atypes) or (players == None):
			e = myembed(title="Match Making", description="**```b.matchmake <solo/duo/trio/squad> <title> [player1] [player2] ...```**", color=get_embed_color())
			await ctx.send(embed=e)
			return
		if ' ' not in players:
			e = myembed(title="Dude, That's Amaing!", description="So, you gona conduct a tourney with 1 player, Nice!\n Make sure to buy brain from BlackMarket before you use this command again!", color=get_embed_color())
			await ctx.send(embed=e)
			return
		tourney = []
		players = players.split(' ')
		rplayers = players
		totalplayers = len(players)
		fixtures = {
		'duo': {'total': 4, 'team': 2},
		'trio': {'total': 6, 'team': 3},
		'squad': {'total': 8, 'team': 4},
		}
		def get_random_player():
			p = random.choice(rplayers)
			rplayers.remove(p)
			return p
		def get_team(n):
			team = []
			for i in range(n):
				team.append(get_random_player())
			return team
		if Type == 'solo':
			remdr = totalplayers % 2
			if totalplayers < 2:
				await ctx.reply(embed=myembed(title="Oops!", description="Insufficient Number of Players for this type of Tourney!", color=get_embed_color()))
				return
			if remdr == 0:
				for i in range(int(totalplayers / 2)):
					p1 = get_random_player()
					p2 = get_random_player()
					mth = {p1: p2}
					tourney.append(mth)
			else:
				for i in range(int((totalplayers - remdr) / 2)):
					p1 = get_random_player()
					p2 = get_random_player()
					mth = {p1: p2}
					tourney.append(mth)
				tourney.append(rplayers)
		else:
			totalp = fixtures[Type]['total']
			teamp = fixtures[Type]['team']
			if totalplayers < totalp:
				await ctx.reply(embed=myembed(title="Oops!", description="Insufficient Number of Players for this type of Tourney!", color=get_embed_color()))
				return
			rmdr = totalplayers % totalp
			if rmdr == 0:
				times = int(totalplayers / totalp)
				for i in range(times):
					t1 = get_team(teamp)
					t2 = get_team(teamp)
					mth = {'t1': t1, 't2': t2}
					tourney.append({'teams': mth})
			else:
				times = int((totalplayers - rmdr) / totalp)
				for i in range(times):
					t1 = get_team(teamp)
					t2 = get_team(teamp)
					mth = {'t1': t1, 't2': t2}
					tourney.append({'teams': mth})
				tourney.append(rplayers)
		des = f"**```\n"
		num = 1
		for match in tourney:
			if isinstance(match, dict):
				for k,v in match.items():
					if isinstance(v, dict):
						team1 = v['t1']
						team2 = v['t2']
						des += f'Match-{str(num)} || '
						for p in team1:
							if p == team1[-1]:
								des += str(p)
							else:
								des += str(p) + ','
						des += ' -v/s- '
						for p in team2:
							if p == team2[-1]:
								des += str(p)
							else:
								des += str(p) + ','
						des += ' ||\n'
					else:
						des += f"Match-{str(num)} || {str(k)} -v/s- {str(v)} ||\n"
					num += 1
			if isinstance(match, list):
				des += f"```**\n ***UnMatchable player(s):***\n**```\n"
				for player in match:
					des += str(player) + '\n'
		des += '```**'
		await ctx.send(embed=myembed(title=title, description=des, color=get_embed_color()))
		return


def setup(bot):
	bot.add_cog(Tournament(bot))