# -*- coding: utf-8 -*-
from discord.ext import commands
from bot.models import server
from bot.db import database


class Servers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__servers = {}

    @commands.Cog.listener()
    async def on_ready(self):
        # add all guilds bot is on to dict of servers
        self.__add_active_servers()

    def __add_active_servers(self):
        """
        Adds all servers using this bot to a dictionary
        (key: guild, value: Server object)
        :return: void
        """
        active_servers = self.bot.guilds

        for guild in active_servers:
            s = server.Server()
            self.add_server(guild, s)

    def add_server(self, guild, serv):
        """
        Adds a server to the dictionary of Servers
        :param guild: guild of server
        :param serv: Server object
        :return: true if added, false if already in
        """
        if self.__servers.get(guild) is None:
            self.__servers[guild] = serv
            return True
        else:
            return False

    def get_server(self, guild):
        """
        Gets server from servers dictionary
        :param guild: guild of server
        :return: Server object
        """
        s = self.__servers.get(guild)
        if s is not None:
            return s
        else:
            raise KeyError('Server not found in servers dict')


def setup(bot):
    bot.add_cog(Servers(bot))

