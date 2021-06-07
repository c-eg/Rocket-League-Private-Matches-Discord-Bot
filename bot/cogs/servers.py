# -*- coding: utf-8 -*-
from discord.ext import commands
from bot.models import server
from bot.models import player
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
        """
        Adds all servers using this bot to a dictionary
        (key: guild, value: Server object)
        :return: void
        """
        active_servers = self.bot.guilds

        for guild in active_servers:
            s = server.Server()
            self.add_server(guild, s)

    def __add_db_players(self):
        """
        Adds all players in database to a dictionary
        (key: discord id, value: Player object)
        :return: void
        """
        sql = 'SELECT * FROM player'
        for row in database.records(sql):
            p = player.Player(row[0], row[1])
            self.add_player(row[0], p)

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

    def add_player(self, discord_id, play):
        """
        Adds a player to the dictionary of players
        :param discord_id: discord id of player
        :param play: Player object
        :return: true if added, false if already in
        """
        if self.__players.get(discord_id) is None:
            self.__players[discord_id] = play
            return True
        else:
            return False

    def get_player(self, discord_id):
        """
        Gets player from players dictionary
        :param discord_id: discord id of player
        :return: Player object
        """
        p = self.__players.get(discord_id)
        if p is not None:
            return p
        else:
            raise KeyError('Player not found in players dict')


def setup(bot):
    bot.add_cog(Servers(bot))

