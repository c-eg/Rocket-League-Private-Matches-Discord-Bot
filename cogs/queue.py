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
        self.users_in_queue = []

    @commands.command(aliases=['q'])
    async def queue(self, ctx: commands.Context):
        # print(ctx.message.channel.name)  # this works btw

        if ctx.author in self.users_in_queue:
            await ctx.channel.send(f'You are already in the queue, {ctx.author.mention}.')
            return

        self.users_in_queue.append(ctx.author)
        embed = embed_template.copy()

        if self.users_in_queue == 1:
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
                name=f'Users in Queue: {str(len(self.users_in_queue))}',
                value=', '.join(user.mention for user in self.users_in_queue),
                inline=False
            )

        await ctx.channel.send(embed=embed)

        # if len(self.users_in_queue) == 6:
        if len(self.users_in_queue) == 1:  # testing
            game_handler = GameHandler(6, self.users_in_queue)
            self.users_in_queue = self.users_in_queue[6:]  # remove users in queue

            loop = asyncio.get_event_loop()
            loop.create_task(self.create_game(ctx, game_handler))

    async def create_game(self, ctx, game_handler):
        """
        TODO:
        - Check to make sure the reaction listener only checks
        the message the bot sent, and no other messages
        """
        embed = embed_template.copy()
        users = game_handler.get_users()

        embed.add_field(
            name='Game Created!',
            value=', '.join(user.mention for user in users),
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

        temp = [user for user in users]

        balanced = 0
        captains = 0
        random = 0

        time_start = time.time() + 20  # should be 120 (2 mins)
        listen_for_reaction = True

        while len(temp) > 0 and listen_for_reaction:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=time_start - time.time(), check=lambda reaction, user: user in users)

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

        if ctx.author in self.users_in_queue:
            self.users_in_queue.remove(ctx.author)

            message.add_field(
                name='User Left the Queue!',
                value=f'{ctx.author.mention} left the queue.',
                inline=False
            )

            if len(self.users_in_queue) > 0:
                message.add_field(
                    name=f'Users in Queue: {str(len(self.users_in_queue))}',
                    value=', '.join(user.mention for user in self.users_in_queue),
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
            await ctx.channel.send(f'You are not in the queue, {ctx.author.mention}')


def setup(bot):
    bot.add_cog(Queue(bot))
