import discord
from discord.ext import commands
from models.server import Server


class Bot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__servers = {}

    @commands.Cog.listener()
    async def on_ready(self):
        # add all guilds bot is on to list of servers
        activeservers = self.bot.guilds

        for guild in activeservers:
            s = Server()
            await self.add_server(guild, s)

    async def add_server(self, guild: discord.Guild, server: Server):
        self.__servers[guild] = server

    async def get_server(self, guild: discord.Guild):
        return self.__servers.get(guild)


def setup(bot):
    bot.add_cog(Bot(bot))
