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

	@commands.group(name='party', invoke_without_command=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def party_cmd(self, ctx):
		t = f"***Available Commands***\n\
		*Note: \n\t (1) The `party_code` is a short identification name, provide a single \
		word like `my_server1`. So that the server can be removed from bot again using that...\
		\n\t (2) The `channel` should be a `channel.mention`, i.e, ping the channel where you want the live stats to be shown\
		\n\t (3) **[Optional]**: The `owner` can be a `user.mention` (i.e, ping the owner) or a string name (eg: `BombSpot Community`)\
		\n\t (4) All Text mustn't contain emojis or special characters*\
		\n\n ~ **Add/Create**:\n```{str(ctx.prefix)}party add <party_code> <#channel> <@owner>```\
		\n ~ **Remove/Del**:\n```{str(ctx.prefix)}party remove <party_code>```"
		e = myembed(title="BombSquad Parties", description=t, color=get_embed_color())
		await ctx.send(embed=e)

	@party_cmd.command(aliases=['create', 'new'])
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def add(self, ctx, party_code: str = None, channel: discord.TextChannel = None, owner=None):
		if (check_server_perms(ctx.author.id)) and ((hasattr(ctx, 'channel')) and (ctx.channel is not None)):
			if channel == None:
				await ctx.reply(f'Invalid args, check the cmd by `{ctx.prefix}party`')
				return
			uid = ctx.author.id
			if owner != None:
				if isinstance(owner, discord.Member): dc_owner = get_clean_user_id(owner.id)
				elif isinstance(owner, str): dc_owner = owner
				else: dc_owner = uid
			else: dc_owner = uid
			try:
				from bp.msg import Msg
				status = {'server_name': party_code, 'server_details': { 'dc_owner': dc_owner, 'chnl': channel.id}}
				Msg().set_process(uid, 'pa_ip', status, self.bot)
				await DMChannel.send(ctx.author, ip_qn)
				await ctx.reply('Check your DM!')
			except Exception as e:
				if type(e) == discord.Forbidden:
					await ctx.reply('Your DM is closed, try this cmd after opening it :O')
				else: print(e)
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
		if (check_server_perms(u)) and ((hasattr(ctx, 'channel')) and (ctx.channel)):
			if party_code == None:
				await ctx.reply("Which party you want to remove nub, Don't waste my time :V")
				return
			servers = get_json('bs_servers')
			if party_code not in servers:
				await ctx.reply("No Live Stats Party exists in this name in Bot's Data :O, check correct code...")
				return
			owners = servers[party_code]['dc_owners']
			if (u not in owners) or (not check_owner_perms(u)):
				peeps = ""
				for p in owners:
					if isinstance(p, int):
						peeps += await get_dc_user_name(self.bot, p) + '\n'
				await ctx.reply(f"You have to be one of these guys:\n```{str(peeps)}```or else **Kill all of them to Take Control of the Server** :V")
				return
			try:
				servers.pop(party_code)
				delete_server(servers)
				return
			except Exception as e:
				ctx.reply(f"Error:```{str(e)}```")
				return
		else:
			await ctx.reply("Sorry, you don't have perms to use this cmd in here!")
			return

def setup(bot):
	bot.add_cog(BombSquadParty(bot))