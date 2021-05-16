from discord.ext import commands
import discord


queue_started = discord.Embed(
    title='Private Matches',
    colour=discord.Colour.dark_red(),
)
queue_started.set_footer(text='Rocket League Private Matches Discord Bot', icon_url='https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/avatars/59/595a3684e667dc05e9d0d7e76efa8bb33b43a45f_full.jpg')


class Queue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def queue(self, ctx: commands.Context):
        server = await self.bot.get_cog('Bot').get_server(ctx.guild)
        await server.add_user(ctx.author)
        users = await server.get_users_in_queue()
        message = queue_started.copy()
        message.add_field(
            name='Queue Started!',
            value=ctx.author.mention + ' has started a queue, type`!q` or `!queue` to join!'
        )
        await ctx.channel.send(embed=message)


def setup(bot):
    bot.add_cog(Queue(bot))
