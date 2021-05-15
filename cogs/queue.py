import discord
from discord.ext import commands


class Queue(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def queue(self, ctx):
        print(ctx.author)


def setup(client):
    client.add_cog(Queue(client))
