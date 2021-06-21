from bp.storage import *
import discord, random, os, json, shutil
from discord import DMChannel
from discord.ext import commands
from datetime import datetime


class Users(commands.Cog):
	"""docstring for Users"""
	def __init__(self, bot):
		self.bot = bot
		self.fap = ""
		self.frp = ""
		self.sap = ""
		self.srp = ""

	@commands.Cog.listener()
	async def on_ready(self):
		print("ServerOwners Cog Running.")

	@commands.command(aliases=['so', 'serverowners'])
	async def server_owners(self, ctx, action: str = None, *, users=None):
		self.bot = ctx.bot
		u = ctx.author.id
		if check_owner_perms(u) == False:
			await ctx.reply("Sorry, you don't have perms to use this cmd!")
			return
		if (users == None) or (action not in ('add', 'remove', 'rm')):
			await ctx.reply(f"***Usage***:\n**```{ctx.prefix}server_owners add/rm/remove <@users>```**")
			return
		try:
			bd = get_json('bot')
			clients = bd['server_owners']
			self.fap = ''
			self.sap = ''
			self.frp = ''
			self.srp = ''
			multi_clients = False
			if isinstance(users, list): multi_clients = True
			async def add(egg):
				c = get_clean_user_id(egg)
				cn = await get_dc_user_name(self.bot, c)
				if c not in clients:
					clients.append(c)
					self.sap += cn + '\n'
				else: self.fap += cn + '\n'
			async def remove(egg):
				c = get_clean_user_id(egg)
				cn = await get_dc_user_name(self.bot, c)
				if c in clients:
					clients.remove(c)
					self.srp += cn + '\n'
				else: self.frp += cn + '\n'
			if action == 'add':
				if multi_clients:
					for client in users:
						await add(client)
				else: await add(users)
			if action in ('rm', 'remove'):
				if multi_clients:
					for client in users:
						await remove(client)
				else: await remove(users)
			e = myembed(title="Bot Config:", color=get_embed_color())
			if self.sap != '': e.add_field(name=f"Successfully added the following clients as `server_owners`:", value=f"```{self.sap}```")
			if self.fap != '': e.add_field(name=f"Failed to add the following clients as `server_owners`:", value=f"```{self.fap}```\nPossible reasons:\n\t- User may already a `server_owner`")
			if self.srp != '': e.add_field(name=f"Successfully removed the following clients from `server_owners`:", value=f"```{self.srp}```")
			if self.frp != '': e.add_field(name=f"Failed to remove the following clients from `server_owners`:", value=f"```{self.frp}```\nPossible reasons:\n\t- User may already not a `server_owner`")
			bd['server_owners'] = clients
			dump_json('bot', bd)
			await ctx.reply(embed=e)
			self.fap = ''
			self.sap = ''
			self.frp = ''
			self.srp = ''
			return
		except Exception as er:
			await ctx.reply(f"Error:```{str(er)}```")
			return

	@commands.command(aliases=['admin'])
	async def admins(self, ctx, action: str = None, *, users=None):
		self.bot = ctx.bot
		u = ctx.author.id
		if check_owner_perms(u) == False:
			await ctx.reply("Sorry, you don't have perms to use this cmd!")
			return
		if (users == None) or (action not in ('add', 'remove', 'rm')):
			await ctx.reply(f"***Usage***:\n**```{ctx.prefix}admins add/rm/remove <@users>```**")
			return
		try:
			bd = get_json('bot')
			clients = bd['admins']
			self.fap = ''
			self.sap = ''
			self.frp = ''
			self.srp = ''
			multi_clients = False
			if isinstance(users, list): multi_clients = True
			async def add(egg):
				c = get_clean_user_id(egg)
				cn = await get_dc_user_name(self.bot, c)
				if c not in clients:
					clients.append(c)
					self.sap += cn + '\n'
				else: self.fap += cn + '\n'
			async def remove(egg):
				c = get_clean_user_id(egg)
				cn = await get_dc_user_name(self.bot, c)
				if c in clients:
					clients.remove(c)
					self.srp += cn + '\n'
				else: self.frp += cn + '\n'
			if action == 'add':
				if multi_clients:
					for client in users:
						await add(client)
				else: await add(users)
			if action in ('rm', 'remove'):
				if multi_clients:
					for client in users:
						await remove(client)
				else: await remove(users)
			e = myembed(title="Bot Config:", color=get_embed_color())
			if self.sap != '': e.add_field(name=f"Successfully added the following clients as `admins`:", value=f"```{self.sap}```")
			if self.fap != '': e.add_field(name=f"Failed to add the following clients as `admins`:", value=f"```{self.fap}```\nPossible reasons:\n\t- User may already a `admins`")
			if self.srp != '': e.add_field(name=f"Successfully removed the following clients from `admins`:", value=f"```{self.srp}```")
			if self.frp != '': e.add_field(name=f"Failed to remove the following clients from `admins`:", value=f"```{self.frp}```\nPossible reasons:\n\t- User may already not a `admins`")
			bd['admins'] = clients
			dump_json('bot', bd)
			await ctx.reply(embed=e)
			self.fap = ''
			self.sap = ''
			self.frp = ''
			self.srp = ''
			return
		except Exception as er:
			await ctx.reply(f"Error:```{str(er)}```")
			return


def setup(bot):
	bot.add_cog(Users(bot))