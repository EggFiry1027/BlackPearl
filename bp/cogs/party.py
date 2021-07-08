from bp.storage import *
import discord, random, os, json, shutil
from discord import DMChannel
from discord.ext import commands
from datetime import datetime

class BombSquadParty(commands.Cog):
	"""docstring for BombSquad"""
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("BombSquadParty Cog Running.")

	@commands.command(aliases=['showparties', 'listparties'])
	async def parties(self, ctx):
		svrs = get_json('bs_servers')
		if svrs == {} or not svrs:
			await ctx.reply("No Servers/Parties are Connected with me!")
			return
		msg = {}
		for s in svrs:
			code = svrs[s]['party_code']
			owners = svrs[s]['dc_owners']
			peeps = []
			for o in owners:
				if isinstance(o, int):
					peeps += await get_dc_user_name(self.bot, o)
				else: peeps += o
			msg[code] = peeps
		emd = myembed(title='List of Parties Connected with me:', description=f"```{str(msg)}```")
		await ctx.reply(embed=emd)

	@commands.group(name='party', invoke_without_command=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def party_cmd(self, ctx):
		t = f"***Available Commands***\n\
		*Note: \n\t (1) The `party_code` is a short identification name, provide a single \
		word like `my_server1`. This is used by stats, top and remove cmds...\
		\n\t (2) The `channel` should be a `channel.mention`, i.e, ping the channel where you want the live stats to be shown\
		\n\t (3) **[Optional]**: The `owner` can be a `user.mention` (i.e, ping the owner) or a string name (eg: `BombSpot Community`)\
		\n\t (4) All Text mustn't contain emojis or special characters*\
		\n\n ~ **Add/Create**:\n```{str(ctx.prefix)}party add <party_code> <#channel> <@owner>```\
		\n ~ **Remove/Del**:\n```{str(ctx.prefix)}party remove <party_code>```"
		e = myembed(title="BombSquad Parties", description=t, color=get_embed_color())
		await ctx.send(embed=e)

	@party_cmd.command(aliases=['create', 'new'])
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def add(self, ctx, party_code: str = None, channel: discord.TextChannel = None, *, owner: list = []):
		if (check_server_perms(ctx.author.id)) and ((hasattr(ctx, 'guild')) and (ctx.guild is not None)):
			if (channel == None) or (not hasattr(channel, 'id')):
				await ctx.reply(f'Invalid Channel, check the cmd by `{ctx.prefix}party`')
				return
			u = ctx.author
			uid = u.id
			servers = get_json('bs_servers')
			if party_code in servers:
				await ctx.reply("A Party already exists with this **`party_code`**!")
				return
			if len(servers) >= 5:
				await ctx.reply("Max Party Limit Reached, sed!")
				return
			dc_owner = []
			if owner != []:
				if isinstance(owner, list):
					for onr in owner:
						if isinstance(onr, discord.Member):
							dc_owner += get_clean_user_id(onr.id)
						elif isinstance(onr, str):
							dc_owner += onr
					dc_owner += uid
				elif isinstance(owner, discord.Member): dc_owner = [get_clean_user_id(owner.id), uid]
				elif isinstance(owner, str): dc_owner = [owner, uid]
				else: dc_owner += uid
			else: dc_owner += uid
			try:
				from bp.msg import Msg
				from bp.livestats import server_embeds
				status = {'server_name': party_code, 'server_details': {'dc_owners': dc_owner, 'dc_admins': [], 'chnl': channel.id}}
				Msg().set_process(uid, 'pa_ip', status, self.bot)
				await DMChannel.send(ctx.author, ip_qn)
				await ctx.reply('Check your DM!')
				server_embeds[party_code] = channel.send(embed=myembed(title=party_code, description=f"***{u.name}#{u.discriminator}*** has started a livestats adding process in this channel!\n Wait for him/her to complete setup!"))
			except Exception as e:
				if type(e) == discord.Forbidden:
					await ctx.reply('Your DM is closed, try this cmd after opening it :O')
				else: await ctx.reply(f"***Error:\n```{str(e)}```***")
		else:
			await ctx.reply("Sorry, you don't have perms to use this cmd in here!")
			return

	@party_cmd.command(aliases=['rm', 'del', 'delete'])
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def remove(self, ctx, party_code: str = None):
		eeee = 'e'
		async def delete_server(s: dict):
			f = bs_servers_path + party_code
			shutil.rmtree(f)
			dump_json('bs_servers', s)
			await ctx.reply("Server Has ***Successfully Removed*** from Bot (Including **`.pem`** file)")
			return

		u = ctx.author.id
		if party_code == None:
			await ctx.reply("Which party you want to remove nub, Don't waste my time :V")
			return
		servers = get_json('bs_servers')
		if party_code not in servers:
			await ctx.reply("No Live Stats Party exists in this name in Bot's Data :O, check correct code...")
			return
		owners = servers[party_code]['dc_owners']
		if (check_owner_perms(u) == True) or (u in owners):
			try:
				servers.pop(party_code)
				await delete_server(servers)
				return
			except Exception as e:
				await ctx.reply(f"***Error:\n```{str(e)}```***")
				return
		else:
			peeps = ""
			for p in owners:
				if isinstance(p, int):
					peeps += await get_dc_user_name(self.bot, p) + '\n'
				else: peeps += p + '\n'
			await ctx.reply(f"You have to be one of these guys:\n***```\n{str(peeps)}```***\nor else **Kill all of them to Take Control of the Server** :V")
			return

def setup(bot):
	bot.add_cog(BombSquadParty(bot))