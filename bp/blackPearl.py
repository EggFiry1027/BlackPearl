from bp.storage import *
import discord, random, os, json, pytz
from bp import mycloud
from discord.ext import commands, tasks
from itertools import cycle
from datetime import datetime

prefix = get_json('bot')['default_prefix']

def get_prefix(bot, message):
	data = get_json('guilds')
	if (message.guild is not None) and (str(message.guild.id) in data):
		return data[str(message.guild.id)]["prefix"]
	else: return prefix

bot = commands.Bot(command_prefix = get_prefix)

#Startup || ONLINE
@bot.event
async def on_ready():
	update_live_stats.start()
	update_server_files.start()
	for file in os.listdir(mydir + 'cogs'):
		if file.endswith('.py'):
			bot.load_extension(f"bp.cogs.{file[:-3]}")
	# await bot.change_presence(activity=discord.Game(f"b.help || Under Testing..."))
	from bp import msg
	print(f"Bot is now Online!, Name = {bot.user.name}#{bot.user.discriminator}, ID = {bot.user.id} || {datetime.now()}")

#GUILD JOIN || Prefix Setup
@bot.event
async def on_guild_join(guild):
	if guild == None or not hasattr(guild, 'id'): return
	data = get_json('guild_data')
	data[str(guild.id)]["prefix"] = prefix
	dump_json('guild_data', data)

@bot.event
async def on_reaction_add(reaction, user):
	if not isinstance(reaction.emoji, str):
		t = f"<:{reaction.emoji.name}:{reaction.emoji.id}>\n"
		with open("emojis.txt", 'a') as f:
			f.write(t)
			f.close()

#MESSAGE
@bot.event
async def on_message(message):
	if message.author == bot.user: return
	from bp import msg
	a = None
	if not message.author.bot: a = await msg.Msg().handle_msg(m=message, bot=bot)
	if a: await a
	if message.content is not None: await bot.process_commands(message)

#Unknown Command Errors Fix
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		ee = random.choice(
			[
			'Egg!','Gae!','Bye Bye!','Hello There!',
			'Bored?, play deathmatch in real life :)',
			'Egg will bite you!','You won\'t feel the taste of an egg!',
			'Dude, That\'s amazing!','RIP egglish :(',
			'I don\'t talk to gaes!','Go away nob bot.'
			]
			)
		await ctx.reply(ee)
		pass
	if isinstance(error, commands.BotMissingPermissions):
		await ctx.reply(f"Error:\n**```{error}```**")
	else: print(error)

#BackGroundTasks
@tasks.loop(seconds=5)
async def update_live_stats():
	#Update Status
	from bp.livestats import LiveStats
	ss = get_json('bs_servers')
	num = len(ss)
	await bot.change_presence(activity=discord.Game(f"b.help || Streaming {num} Server/Party(s) Live Stats :P"))
	#Update Server Live Stats
	await LiveStats().update_live()

@tasks.loop(seconds=300)
async def update_server_files():
	#Update stats.json and players.json of all servers
	mycloud.SFTP().update_stats()
	mycloud.SFTP().update_players()