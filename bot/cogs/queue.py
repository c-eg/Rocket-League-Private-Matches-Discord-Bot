import discord
from discord.ext import commands

queue_message = discord.Embed(
    title='Private Matches',
    colour=discord.Colour.dark_red()
)
queue_message.set_footer(
    text='Rocket League Private Matches Discord Bot',
    icon_url='https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/avatars/59/595a3684e667dc05e9d0d7e76efa8bb33b43a45f_full.jpg'
)


class Queue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['q'])
    async def queue(self, ctx: commands.Context):
        # player = Player()

        server = self.bot.get_cog('Servers').get_server(ctx.guild)  # get server user is on
        server.add_user(ctx.author)  # add user to server's queue

        users = server.get_users_in_queue()
        message = queue_message.copy()

        if len(users) == 1:
            message.add_field(
                name='Queue Started!',
                value=ctx.author.mention + ' has started a queue, type `;q` or `;queue` to join!',
                inline = False
            )
        elif 1 < len(users) < server.get_game_size():
            message.add_field(
                name='User Joined Queue!',
                value=ctx.author.mention + ' joined the queue.',
                inline=False
            )
            message.add_field(
                name='Users in Queue: ' + str(len(users)),
                value=', '.join(user.mention for user in users),
                inline=False
            )
        else:
            pass
            # create game

        await ctx.channel.send(embed=message)

    @commands.command(aliases=['l'])
    async def leave(self, ctx: commands.Context):
        server = self.bot.get_cog('Servers').get_server(ctx.guild)  # get server user is on
        server.remove_user(ctx.author)  # add user to server's queue

        # TODO: make message embed for user left

        message = queue_message.copy()

        await ctx.channel.send(embed=message)


def setup(bot):
    bot.add_cog(Queue(bot))




