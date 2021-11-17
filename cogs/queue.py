# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

from collections import OrderedDict
import time
import asyncio
from models.no_player_action_exception import NoPlayerActionException

from models.player import Player
from models.game_handler import GameHandler
from models.game_balanced import BalancedGame
from models.game_captains import CaptainsGame
from models.game_random import RandomGame
from db.database import record

embed_template = discord.Embed(
    title='Private Matches',
    colour=discord.Colour.teal()
)
embed_template.set_footer(
    text='UEA Private Matches by curpha',
    icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars/be/bed810f8bebd7be235b8f7176e3870de1006a6e5_full.jpg'
)


class Queue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.users_in_queue = OrderedDict()

    @commands.command(aliases=['q'])
    async def queue(self, ctx: commands.Context):
        if ctx.channel.name != '6-mans-test-things':
            return

        if self.users_in_queue.get(ctx.author.id, False):
            await ctx.channel.send(f'You are already in the queue, {ctx.author.mention}.')
            return

        res = record("SELECT * FROM player WHERE discord_id = ?", ctx.author.id)

        if res is None:
            await ctx.channel.send(f'You have not set your mmr, please use: `;setpeak <amount>`!\n\nIf you need to find what your mmr is, go here: https://rocketleague.tracker.network/')
            return

        self.users_in_queue[ctx.author.id] = Player(ctx.author, res[1])

        embed = embed_template.copy()

        if len(self.users_in_queue) == 1:
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
                value=', '.join(player.get_discord_user().mention for player in self.users_in_queue.values()),
                inline=False
            )

        await ctx.channel.send(embed=embed)

        if len(self.users_in_queue) == 6:
            game_players = []

            for i in range(6):
                game_players.append(self.users_in_queue.popitem(last=False)[1])

            game_handler = GameHandler(6, game_players)

            loop = asyncio.get_event_loop()
            loop.create_task(self.create_game(ctx, game_handler))

    async def create_game(self, ctx, game_handler):
        """
        Creates a game for the users who are in the queue.
        """
        embed = embed_template.copy()
        players = game_handler.get_players()

        embed.add_field(
            name='Users to Vote!',
            value=', '.join(player.get_discord_user().mention for player in players),
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

        users_voting = [player.get_discord_user() for player in players]

        balanced = 0
        captains = 0
        random = 0

        time_start = time.time() + 120
        listen_for_reaction = True

        def check(reaction, user):
            return user in users_voting and message == reaction.message

        while len(users_voting) > 0 and listen_for_reaction:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=time_start - time.time(), check=check)

                if reaction.emoji == "🇧":
                    balanced += 1
                elif reaction.emoji == "🇨":
                    captains += 1
                elif reaction.emoji == "🇷":
                    random += 1

                if user in users_voting:
                    users_voting.remove(user)
            except asyncio.TimeoutError:
                listen_for_reaction = False

        if balanced > captains and balanced > random:
            game = BalancedGame(players)
        elif captains > balanced and captains > random:
            game = CaptainsGame(players, ctx, self.bot)
        else:
            game = RandomGame(players)

        try:
            await game.assign_teams()
        except NoPlayerActionException:
            await ctx.channel.send("A user did not complete their task in enough time. Game is cancelled.")
            return

        embed = embed_template.copy()

        embed.add_field(
            name='Team 1',
            value=', '.join(player.get_discord_user().mention for player in game.get_team_one()),
            inline=False
        )
        embed.add_field(
            name='Team 2',
            value=', '.join(player.get_discord_user().mention for player in game.get_team_two()),
            inline=False
        )

        await ctx.channel.send(embed=embed)

    @commands.command(aliases=['l'])
    async def leave(self, ctx: commands.Context):
        if ctx.channel.name != '6-mans-test-things':
            return

        embed = embed_template.copy()

        if not self.users_in_queue.get(ctx.author.id, False):
            await ctx.channel.send(f'You are not in the queue, {ctx.author.mention}')
            return

        del self.users_in_queue[ctx.author.id]

        embed.add_field(
            name='User Left the Queue!',
            value=f'{ctx.author.mention} left the queue.',
            inline=False
        )

        if len(self.users_in_queue) > 0:
            embed.add_field(
                name=f'Users in Queue: {str(len(self.users_in_queue))}',
                value=', '.join(player.get_discord_user().mention for player in self.users_in_queue.values()),
                inline=False
            )
        else:
            embed.add_field(
                name=f'Queue Empty!',
                value='To restart the queue, type `;q` or `;queue`',
                inline=False
            )

        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context):
        if ctx.channel.name != '6-mans-test-things':
            return

        self.users_in_queue.clear()

        embed = embed_template.copy()

        embed.add_field(
            name='The queue has been cleared!',
            value='Please type `;q` or `;queue` to restart the queue.',
            inline=False
        )

        await ctx.channel.send(embed=embed)

    @clear.error
    async def clear_error(self, error, ctx):
        if isinstance(error, error.MissingPermissions):
            await ctx.send("You do not have permission to use `;clear`!")
        else:
            raise error


def setup(bot):
    bot.add_cog(Queue(bot))
