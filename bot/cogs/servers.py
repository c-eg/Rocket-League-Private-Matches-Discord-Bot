# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from bot.models import server
from bot.db import database


class Servers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__servers = {}
        self.__players = {}

    @commands.Cog.listener()
    async def on_ready(self):
        # add all guilds bot is on to list of servers
        self.__add_active_servers()
        self.__add_db_players()

    def __add_active_servers(self):
        activeservers = self.bot.guilds

        for guild in activeservers:
            s = server.Server()
            self.add_server(guild, s)

    def __add_db_players(self):
        sql = 'SELECT * FROM player'
        for row in database.records(sql):
            self.__players[row[0]] = row[1]

    def add_server(self, guild: discord.Guild, server: server.Server):
        self.__servers[guild] = server

    def get_server(self, guild: discord.Guild):
        return self.__servers.get(guild)


def setup(bot):
    bot.add_cog(Servers(bot))
