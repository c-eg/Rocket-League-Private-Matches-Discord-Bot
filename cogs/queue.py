# -*- coding: utf-8 -*-
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
        print(ctx.message.channel.name)  # this works btw

        four, six = self.bot.get_cog('Servers').get_game_handlers(ctx.guild)  # get game handlers
        added = six.add_user(ctx.author)
        
        message = queue_message.copy()

        if added is True:
            users_in_queue = six.get_users_in_queue()

            if users_in_queue == 1:
                message.add_field(
                    name='Queue Started!',
                    value=ctx.author.mention + ' has started a queue, type `;q` or `;queue` to join!',
                    inline=False
                )
            else:
                message.add_field(
                    name='User Joined Queue!',
                    value=ctx.author.mention + ' joined the queue, type `;q` or `;queue` to join!',
                    inline=False
                )
                message.add_field(
                    name='Users in Queue: ' + str(len(users_in_queue)),
                    value=', '.join(user.mention for user in users_in_queue),
                    inline=False
                )

            if six.check_queue() is True:
                # TODO: maybe make this async so users can queue while others are voting?
                # maybe a way of doing this would be to make an async function in this file
                # which sends a message and awaits for user votes
                #    would probs need a reaction listener or something
                # 
                game = six.create_game()

            await ctx.channel.send(embed=message)

        """
        Message to future me working on this:
        - Figure out how to create a game and handle the voting stuff
            without preventing other users using commands
        - For voting, get the reaction system to work (looks good)
        - Future: add 4 man handling (currently only doing 6)
        """

    @commands.command(aliases=['l'])
    async def leave(self, ctx: commands.Context):
        server = self.bot.get_cog('Servers').get_server(ctx.guild)  # get server user is on
        server.remove_user(ctx.author)  # add user to server's queue

        # TODO: make message embed for user left

        message = queue_message.copy()

        await ctx.channel.send(embed=message)


def setup(bot):
    bot.add_cog(Queue(bot))
