import discord
from discord.ext import commands


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = []

    @commands.command()
    async def queue(self, ctx):
        self.users.append(ctx.author)
        temp = ', '.join(user.name for user in self.users)

        await ctx.send(temp)


def setup(bot):
    bot.add_cog(Queue(bot))
