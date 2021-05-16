import discord
from discord.ext import commands


class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leave(self, ctx):
        pass
        # TODO: implement this


def setup(bot):
    bot.add_cog(Leave(bot))
