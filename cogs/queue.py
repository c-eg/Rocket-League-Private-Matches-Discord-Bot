import discord
from discord.ext import commands
import models.server


class Queue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def queue(self, ctx: commands.Context):
        server = await self.bot.get_cog('Bot').get_server(ctx.guild)
        await server.add_user(ctx.author)
        users = await server.get_users_in_queue()
        await ctx.send(str(users))


def setup(bot):
    bot.add_cog(Queue(bot))
