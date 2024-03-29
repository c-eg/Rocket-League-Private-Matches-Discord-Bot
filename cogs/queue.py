# -*- coding: utf-8 -*-

import asyncio
import os
import time
from collections import OrderedDict

import discord
from db.database import record
from discord.commands import Option, slash_command
from discord.ext import commands
from models.game_balanced import BalancedGame
from models.game_captains import CaptainsGame
from models.game_handler import GameHandler
from models.game_random import RandomGame
from models.no_player_action_exception import NoPlayerActionException
from models.player import Player
import logging


logger = logging.getLogger(__name__)


class Queue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.users_in_queue = OrderedDict()

    async def _remove_user(self, ctx: commands.Context, minutes: int):
        if self.users_in_queue.get(ctx.author.id, False):
            logger.info(f"{ctx.author} set a timer to remove them from the queue after {minutes} minutes")
            await asyncio.sleep(minutes * 60)
            await ctx.invoke(self.bot.get_command("leave"))

    @slash_command(description="Joins the private matches queue.")
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def queue(
        self,
        ctx: commands.Context,
        time_to_queue: Option(int, "Time to queue", required=False, min_value=1),
    ):
        if ctx.channel.name != os.environ.get("6_MAN_CHANNEL"):
            return

        if self.users_in_queue.get(ctx.author.id, False):
            await ctx.respond(f"You are already in the queue, {ctx.author.mention}.")
            return

        res = record("SELECT * FROM player WHERE discord_id = ?", ctx.author.id)

        if res is None:
            await ctx.respond(
                f"You have not set your mmr, please use: `/setpeak <amount>`!\n\nIf you need to find what your mmr is, go here: https://rocketleague.tracker.network/"
            )
            return

        # add user to queue
        self.users_in_queue[ctx.author.id] = Player(ctx.author, res[1])
        logger.info(f"User: {ctx.author} joined the queue")

        # if the user only wants to queue for a certain amount of time, create task to remove from queue after time has passed
        if time_to_queue:
            asyncio.gather(self._remove_user(ctx, time_to_queue))

        embed = discord.Embed(
            title="Rocket League Private Matches", colour=discord.Colour.teal()
        )

        if len(self.users_in_queue) == 1:
            embed.add_field(
                name="Queue Started!",
                value=f"{ctx.author.mention} has started a queue, type `/queue` to join!",
                inline=False,
            )
        else:
            embed.add_field(
                name="User Joined the Queue!",
                value=f"{ctx.author.mention} joined the queue, type `/queue` to join!",
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

        await ctx.respond(embed=embed)

        if len(self.users_in_queue) == 6:
            game_players = []

            for i in range(6):
                game_players.append(self.users_in_queue.popitem(last=False)[1])

            game_handler = GameHandler(6, game_players)

            await self.create_game(ctx, game_handler)

    async def create_game(self, ctx: commands.Context, game_handler: GameHandler):
        """
        Creates a game for the users who are in the queue.
        """
        users_voting = [player.get_discord_user() for player in players]
        logger.info(f"Game started with users: {users_voting}")
        
        embed = discord.Embed(
            title="Rocket League Private Matches", colour=discord.Colour.teal()
        )
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
        message = await ctx.respond(embed=embed)
        await message.add_reaction("🇧")
        await message.add_reaction("🇨")
        await message.add_reaction("🇷")

        balanced_count = 0
        captains_count = 0
        random_count = 0

        votes = {}
        users_not_voted = [player.get_discord_user() for player in players]

        time_start = time.time() + 120
        listen_for_reaction = True

        def check(reaction: discord.Reaction, user: discord.User) -> bool:
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

                new_embed = discord.Embed(
                    title="Rocket League Private Matches", colour=discord.Colour.teal()
                )

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
            await ctx.respond(
                "A user did not complete their task in enough time. Game is cancelled."
            )
            return

        embed = discord.Embed(
            title="Rocket League Private Matches", colour=discord.Colour.teal()
        )

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

        await ctx.respond(embed=embed)

    @slash_command(description="Leaves the private matches queue.")
    async def leave(self, ctx: commands.Context):
        if ctx.channel.name != os.environ.get("6_MAN_CHANNEL"):
            return

        embed = discord.Embed(
            title="Rocket League Private Matches", colour=discord.Colour.teal()
        )

        if not self.users_in_queue.get(ctx.author.id, False):
            await ctx.respond(f"You are not in the queue, {ctx.author.mention}")
            return

        del self.users_in_queue[ctx.author.id]

        logger.info(f"User: {ctx.author} left the queue")

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
                value=f"To restart the queue, type `/queue`",
                inline=False,
            )

        await ctx.respond(embed=embed)

    @commands.slash_command(
        description="Lists all the users in the private matches queue."
    )
    async def list(self, ctx: commands.Context):
        if ctx.channel.name != os.environ.get("6_MAN_CHANNEL"):
            return

        embed = discord.Embed(
            title="Rocket League Private Matches", colour=discord.Colour.teal()
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
                value=f"To start the queue, type `/queue`",
                inline=False,
            )

        await ctx.respond(embed=embed)

    @slash_command(description="Clears all users from the queue.")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context):
        if ctx.channel.name != os.environ.get("6_MAN_CHANNEL"):
            return

        self.users_in_queue.clear()
        logger.info(f"{ctx.author} cleared the queue")

        embed = discord.Embed(
            title="Rocket League Private Matches", colour=discord.Colour.teal()
        )

        embed.add_field(
            name="The queue has been cleared!",
            value=f"Please type `/queue` to restart the queue.",
            inline=False,
        )

        await ctx.respond(embed=embed)

    @clear.error
    async def clear_error(self, error, ctx: commands.Context):
        if isinstance(error, error.MissingPermissions):
            await ctx.send(f"You do not have permission to use `/clear`")
        else:
            raise error


def setup(bot: commands.Bot):
    bot.add_cog(Queue(bot))
