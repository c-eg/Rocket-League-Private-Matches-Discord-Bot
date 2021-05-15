import discord
from discord.ext import commands


class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leave(self, ctx):
        users = self.bot.get_cog('Queue').users
        temp = ', '.join(user.name for user in users)
        await ctx.send(temp)


def setup(bot):
    bot.add_cog(Leave(bot))
