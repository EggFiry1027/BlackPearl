from bp.storage import *
import discord, random, os, json, pytz
from bp import mycloud
from discord.ext import commands
from itertools import cycle
from datetime import datetime

class Utility(commands.Cog):
	"""docstring for Utility"""
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("Utility Cog Running.")

	@commands.command()
	async def ping(self, ctx):
		l = str(float(ctx.bot.latency*1000))
		lm = f"**Pong!, `{l.split('.')[0]}.{l.split('.')[1][:2]}ms`**"
		await ctx.send(lm)

	@commands.command()
	async def whois(self, ctx, aid: str = None):
		if aid == None:
			await ctx.reply("Send pb-ID/account_id as an arg :/")
			return
		try:
			url = 'http://bombsquadgame.com/accountquery?id=' + aid
			data = get_response(url).decode()
			if isinstance(data, dict):
				out = f"```json\n{str(data)}```"
			else:
				out = f"```{str(data)}```"
			await ctx.reply(content=out)
		except Exception as e:
			await ctx.reply(f"Error:\n```{str(e)}```")

	@commands.command()
	async def say(self, ctx, *, t: str = None):
		if t != None: await ctx.send(t)
		else: await ctx.reply('What to say?')

	@commands.command(aliases=['de', 'dumpemojis'])
	async def dump_emojis(self, ctx):
		if not hasattr(ctx, 'guild'):
			await ctx.reply("This is not a Channel From Server!")
			return
		try:
			ejs = ctx.guild.emojis
			if len(ejs) >= 1:
				a = {i.name: i.id for i in ejs}
				fn = temp_folder + f'emojis_{ctx.guild.id}.json'
				dump_json(fn, a, temp=True)
				await ctx.send(file=discord.File(fn))
				os.remove(fn)
			else:
				await ctx.reply("No Emojies in This Server, sed :O")
		except Exception as e:
			await ctx.reply(f"Error:\n```{str(e)}```")

def setup(bot):
	bot.add_cog(Utility(bot))