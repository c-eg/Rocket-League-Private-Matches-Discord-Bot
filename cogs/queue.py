# -*- coding: utf-8 -*-

import discord
from discord import client
from discord.ext import commands
from discord.ext.commands import Cog

from models.game_handler import GameHandler

import time
import asyncio

embed_template = discord.Embed(
    title='Private Matches',
    colour=discord.Colour.dark_red()
)
embed_template.set_footer(
    text='Bot created by curpha',
    icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars/be/bed810f8bebd7be235b8f7176e3870de1006a6e5_full.jpg'
)


class Queue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.game_handler = GameHandler(6)

    @commands.command(aliases=['q'])
    async def queue(self, ctx: commands.Context):
        # print(ctx.message.channel.name)  # this works btw

        added = self.game_handler.add_user(ctx.author)

        if added is True:
            users_in_queue = self.game_handler.get_users_in_queue()
            embed = embed_template.copy()

            if users_in_queue == 1:
                embed.add_field(
                    name='Queue Started!',
                    value=f'{ctx.author.mention} has started a queue, type `;q` or `;queue` to join!',
                    inline=False
                )
            else:
                embed.add_field(
                    name='User Joined the Queue!',
                    value=f'{ctx.author.mention} joined the queue, type `;q` or `;queue` to join!',
                    inline=False
                )
                embed.add_field(
                    name=f'Users in Queue: {str(len(users_in_queue))}',
                    value=', '.join(user.mention for user in users_in_queue),
                    inline=False
                )

            await ctx.channel.send(embed=embed)

            # if self.game_handler.check_queue() is True:
            if len(users_in_queue) == 1:  # testing
                # game = self.game_handler.create_game()
                loop = asyncio.get_event_loop()
                loop.create_task(self.create_game(ctx, users_in_queue))

    async def create_game(self, ctx, users_in_queue):
        """
        TODO:
        - Maybe change users_in_queue to a GameHandler object?
            - because users_in_queue is passed as a reference, not value
        """
        embed = embed_template.copy()

        embed.add_field(
            name='Game Created!',
            value=', '.join(user.mention for user in users_in_queue),
            inline=False
        )

        embed.add_field(
            name='Vote for Balancing Method!!',
            value=f'🇧 for Balanced Teams\n\n🇨 for Captains\n\n🇷 for Random Teams',
            inline=False
        )

        message = await ctx.channel.send(embed=embed)
        await message.add_reaction("🇧")
        await message.add_reaction("🇨")
        await message.add_reaction("🇷")

        temp = []
        for user in users_in_queue:
            temp.append(user)

        balanced = 0
        captains = 0
        random = 0

        time_start = time.time() + 20  # should be 120 (2 mins)
        listen_for_reaction = True

        while len(temp) > 0 and listen_for_reaction:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=time_start - time.time(), check=lambda reaction, user: user in users_in_queue)

                if reaction.emoji == "🇧":
                    balanced += 1
                elif reaction.emoji == "🇨":
                    captains += 1
                elif reaction.emoji == "🇷":
                    random += 1

                print(f'user: {user}, reaction: {reaction}')

                # if user in temp:
                #     temp.remove(user)
            except asyncio.TimeoutError:
                listen_for_reaction = False

        print('\ntime ran out\n')

    @commands.command(aliases=['l'])
    async def leave(self, ctx: commands.Context):
        message = embed_template.copy()
        users_in_queue = self.game_handler.get_users_in_queue()

        if ctx.author in users_in_queue:
            self.game_handler.remove_user(ctx.author)  # remove user from queue

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
