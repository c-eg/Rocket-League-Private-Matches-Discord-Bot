# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

message_template = discord.Embed(
    title='Private Matches',
    colour=discord.Colour.dark_red()
)
message_template.set_footer(
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

        message = message_template.copy()

        if added is True:
            users_in_queue = six.get_users_in_queue()

            if users_in_queue == 1:
                message.add_field(
                    name='Queue Started!',
                    value=f'{ctx.author.mention} has started a queue, type `;q` or `;queue` to join!',
                    inline=False
                )
            else:
                message.add_field(
                    name='User Joined the Queue!',
                    value=f'{ctx.author.mention} joined the queue, type `;q` or `;queue` to join!',
                    inline=False
                )
                message.add_field(
                    name=f'Users in Queue: {str(len(users_in_queue))}',
                    value=', '.join(user.mention for user in users_in_queue),
                    inline=False
                )

            if six.check_queue() is True:
                game = six.create_game()

                # send message with votes

                # listen for votes

                # set timer for 2 mins

            await ctx.channel.send(embed=message)

    @commands.command(aliases=['l'])
    async def leave(self, ctx: commands.Context):
        four, six = self.bot.get_cog('Servers').get_game_handlers(ctx.guild)  # get game handlers

        message = message_template.copy()
        users_in_queue = six.get_users_in_queue()

        if ctx.author in users_in_queue:
            six.remove_user(ctx.author)  # remove user from queue

            message.add_field(
                name='User Left the Queue!',
                value=f'{ctx.author.mention} left the queue.',
                inline=False
            )

            if len(users_in_queue) > 0:
                message.add_field(
                    name=f'Users in Queue: {str(len(users_in_queue))}',
                    value=', '.join(user.mention for user in users_in_queue),
                    inline=False
                )
            else:
                message.add_field(
                    name=f'Queue Empty!',
                    value='To restart the queue, type `;q` or `;queue`',
                    inline=False
                )

            await ctx.channel.send(embed=message)
        else:
            await ctx.channel.send(f'You are not in the queue {ctx.author.mention}')


def setup(bot):
    bot.add_cog(Queue(bot))
