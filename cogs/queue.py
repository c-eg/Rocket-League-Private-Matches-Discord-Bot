# -*- coding: utf-8 -*-

import asyncio
import os
import time
from collections import OrderedDict

import discord
from db.database import record
from discord.ext import commands
from models.game_balanced import BalancedGame
from models.game_captains import CaptainsGame
from models.game_handler import GameHandler
from models.game_random import RandomGame
from models.no_player_action_exception import NoPlayerActionException
from models.player import Player
from static.embed_template import EmbedTemplate

embed_template = EmbedTemplate(title="Private Matches", colour=discord.Colour.teal())


class Queue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.users_in_queue = OrderedDict()

    async def _remove_user(self, ctx, minutes):
        if self.users_in_queue.get(ctx.author.id, False):
            await asyncio.sleep(minutes * 60)
            await ctx.invoke(self.bot.get_command("leave"))

    @commands.command(
        aliases=["q"], help="Joins the private matches queue.", brief="Joins the queue."
    )
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def queue(self, ctx: commands.Context, time_to_queue: int = None):
        if ctx.channel.name != os.environ.get("6_MAN_CHANNEL"):
            return

        if self.users_in_queue.get(ctx.author.id, False):
            await ctx.channel.send(
                f"You are already in the queue, {ctx.author.mention}."
            )
            return

        prefix = await self.bot.get_prefix(ctx.message)
        res = record("SELECT * FROM player WHERE discord_id = ?", ctx.author.id)

        if res is None:
            await ctx.channel.send(
                f"You have not set your mmr, please use: `{prefix}setpeak <amount>`!\n\nIf you need to find what your mmr is, go here: https://rocketleague.tracker.network/"
            )
            return

        # add user to queue
        self.users_in_queue[ctx.author.id] = Player(ctx.author, res[1])

        # if user is only in queue for certain amount of time, create task to check in said time
        if time_to_queue is not False and time_to_queue > 0:
            asyncio.gather(self._remove_user(ctx, time_to_queue))

        embed = embed_template.copy()

        if len(self.users_in_queue) == 1:
            embed.add_field(
                name="Queue Started!",
                value=f"{ctx.author.mention} has started a queue, type `{prefix}q` or `{prefix}queue` to join!",
                inline=False,
            )
        else:
            embed.add_field(
                name="User Joined the Queue!",
                value=f"{ctx.author.mention} joined the queue, type `{prefix}q` or `{prefix}queue` to join!",
                inline=False,
            )
            embed.add_field(
                name=f"Users in Queue: {str(len(self.users_in_queue))}",
                value=", ".join(
                    player.get_discord_user().mention
                    for player in self.users_in_queue.values()
                ),
                inline=False,
            )

        await ctx.channel.send(embed=embed)

        if len(self.users_in_queue) == 6:
            game_players = []

            for i in range(6):
                game_players.append(self.users_in_queue.popitem(last=False)[1])

            game_handler = GameHandler(6, game_players)

            await self.create_game(ctx, game_handler)

    async def create_game(self, ctx, game_handler):
        """
        Creates a game for the users who are in the queue.
        """
        embed = embed_template.copy()
        players = game_handler.get_players()

        embed.add_field(
            name="Users to Vote!",
            value=", ".join(player.get_discord_user().mention for player in players),
            inline=False,
        )
        embed.add_field(
            name="Vote for Balancing Method!!",
            value=f"🇧 for Balanced Teams\n\n🇨 for Captains\n\n🇷 for Random Teams",
            inline=False,
        )

        # add reactions to message
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction("🇧")
        await message.add_reaction("🇨")
        await message.add_reaction("🇷")

        users_voting = [player.get_discord_user() for player in players]

        balanced_count = 0
        captains_count = 0
        random_count = 0

        votes = {}
        users_not_voted = [player.get_discord_user() for player in players]

        time_start = time.time() + 120
        listen_for_reaction = True

        def check(reaction, user):
            """Check to process reaction"""
            reactions = ["🇧", "🇨", "🇷"]

            if (
                user not in users_voting
                or message != reaction.message
                or reaction.emoji not in reactions
            ):
                return False

            return True

        # listen for reactions on the message from users in the game
        while listen_for_reaction:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=time_start - time.time(), check=check
                )

                # remove user from users not voted
                if user in users_not_voted:
                    users_not_voted.remove(user)

                # remove old vote
                old_vote = votes.get(user)

                if old_vote:
                    if old_vote == "🇧":
                        balanced_count -= 1
                    elif old_vote == "🇨":
                        captains_count -= 1
                    elif old_vote == "🇷":
                        random_count -= 1

                # add new vote
                votes[user] = reaction.emoji

                if reaction.emoji == "🇧":
                    balanced_count += 1
                elif reaction.emoji == "🇨":
                    captains_count += 1
                elif reaction.emoji == "🇷":
                    random_count += 1

                # remove reaction from message
                await reaction.remove(user)

                # update message with users who voted for what
                balanced = ", ".join(
                    user.mention for user, vote in votes.items() if vote == "🇧"
                )
                captains = ", ".join(
                    user.mention for user, vote in votes.items() if vote == "🇨"
                )
                random = ", ".join(
                    user.mention for user, vote in votes.items() if vote == "🇷"
                )

                new_embed = embed_template.copy()

                new_embed.add_field(
                    name="Users to Vote!",
                    value=", ".join(user.mention for user in users_not_voted),
                    inline=False,
                )
                new_embed.add_field(
                    name="Vote for Balancing Method!!",
                    value=f"🇧 for Balanced Teams\n{balanced}\n\n🇨 for Captains\n{captains}\n\n🇷 for Random Teams\n{random}",
                    inline=False,
                )

                await message.edit(embed=new_embed)

                if balanced_count == 4 or captains_count == 4 or random_count == 4:
                    listen_for_reaction = False
            except asyncio.TimeoutError:
                listen_for_reaction = False

        if balanced_count > captains_count and balanced_count > random_count:
            game = BalancedGame(players)
        elif captains_count > balanced_count and captains_count > random_count:
            game = CaptainsGame(players, ctx, self.bot)
        else:
            game = RandomGame(players)

        try:
            await game.assign_teams()
        except NoPlayerActionException:
            await ctx.channel.send(
                "A user did not complete their task in enough time. Game is cancelled."
            )
            return

        embed = embed_template.copy()

        embed.add_field(
            name="Team 1",
            value=", ".join(
                player.get_discord_user().mention for player in game.get_team_one()
            ),
            inline=False,
        )
        embed.add_field(
            name="Team 2",
            value=", ".join(
                player.get_discord_user().mention for player in game.get_team_two()
            ),
            inline=False,
        )

        await ctx.channel.send(embed=embed)

    @commands.command(
        aliases=["l"],
        help="Leaves the private matches queue.",
        brief="Leaves the queue.",
    )
    async def leave(self, ctx: commands.Context):
        if ctx.channel.name != os.environ.get("6_MAN_CHANNEL"):
            return

        prefix = await self.bot.get_prefix(ctx.message)
        embed = embed_template.copy()

        if not self.users_in_queue.get(ctx.author.id, False):
            await ctx.channel.send(f"You are not in the queue, {ctx.author.mention}")
            return

        del self.users_in_queue[ctx.author.id]

        embed.add_field(
            name="User Left the Queue!",
            value=f"{ctx.author.mention} left the queue.",
            inline=False,
        )

        if len(self.users_in_queue) > 0:
            embed.add_field(
                name=f"Users in Queue: {str(len(self.users_in_queue))}",
                value=", ".join(
                    player.get_discord_user().mention
                    for player in self.users_in_queue.values()
                ),
                inline=False,
            )
        else:
            embed.add_field(
                name=f"Queue Empty!",
                value=f"To restart the queue, type `{prefix}q` or `{prefix}queue`",
                inline=False,
            )

        await ctx.channel.send(embed=embed)

    @commands.command(
        help="Lists all the users in the private matches queue.",
        brief="Lists users in the queue.",
    )
    async def list(self, ctx: commands.Context):
        if ctx.channel.name != os.environ.get("6_MAN_CHANNEL"):
            return

        prefix = await self.bot.get_prefix(ctx.message)
        embed = embed_template.copy()

        if len(self.users_in_queue) > 0:
            embed.add_field(
                name=f"Users in Queue: {str(len(self.users_in_queue))}",
                value=", ".join(
                    player.get_discord_user().mention
                    for player in self.users_in_queue.values()
                ),
                inline=False,
            )
        else:
            embed.add_field(
                name=f"Queue Empty!",
                value=f"To start the queue, type `{prefix}q` or `{prefix}queue`",
                inline=False,
            )

        await ctx.channel.send(embed=embed)

    @commands.command(
        help="Clears all users from the queue.", brief="Clears the queue."
    )
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context):
        if ctx.channel.name != os.environ.get("6_MAN_CHANNEL"):
            return

        self.users_in_queue.clear()

        prefix = await self.bot.get_prefix(ctx.message)
        embed = embed_template.copy()

        embed.add_field(
            name="The queue has been cleared!",
            value=f"Please type `{prefix}q` or `{prefix}queue` to restart the queue.",
            inline=False,
        )

        await ctx.channel.send(embed=embed)

    @clear.error
    async def clear_error(self, error, ctx):
        prefix = await self.bot.get_prefix(ctx.message)

        if isinstance(error, error.MissingPermissions):
            await ctx.send(f"You do not have permission to use `{prefix}clear`")
        else:
            raise error

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def tq(self, ctx: commands.Context):
    #     if ctx.channel.name != os.environ.get('6_MAN_CHANNEL'):
    #         return

    #     user_one = await self.bot.fetch_user(260169773357203456)
    #     user_two = await self.bot.fetch_user(199583437764427777)
    #     user_three = await self.bot.fetch_user(386283781436211211)
    #     user_four = await self.bot.fetch_user(190198777334857728)
    #     user_five = await self.bot.fetch_user(684864344072519681)

    #     self.users_in_queue[user_one.id] = Player(user_one, 200)
    #     self.users_in_queue[user_two.id] = Player(user_two, 300)
    #     self.users_in_queue[user_three.id] = Player(user_three, 100)
    #     self.users_in_queue[user_four.id] = Player(user_four, 50)
    #     self.users_in_queue[user_five.id] = Player(user_five, 250)


def setup(bot):
    bot.add_cog(Queue(bot))
