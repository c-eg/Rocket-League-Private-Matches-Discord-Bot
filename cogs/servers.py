# -*- coding: utf-8 -*-
from discord.ext import commands
from models.game_handler import GameHandler


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
        (key: guild, value: [GameHandler, GameHandler])
        :return: void
        """
        active_servers = self.bot.guilds

        for guild in active_servers:
            self.add_guild(guild)

    def add_guild(self, guild):
        """
        Adds a server to the dictionary
        :param guild: guild of server
        :return: true if added, false if already in
        """
        if self.__servers.get(guild) is None:
            four = GameHandler(4)  # 4 man queue
            six = GameHandler(6)  # 6 man queue

            self.__servers[guild] = [four, six]
            return True

        return False

    def get_guild(self, guild):
        """
        Gets GameHandler(s) from dictionary
        :param guild: guild of server
        :return: list of GameHandler objects
        """
        four, six = self.__servers.get(guild)

        if four is not None and six is not None:
            return four, six
        else:
            raise KeyError('Server not found in servers dict')


def setup(bot):
    bot.add_cog(Servers(bot))
