# -*- coding: utf-8 -*-

import os

import discord
from db import database
from discord.commands import Option, slash_command
from discord.ext import commands
from static.embed_template import EmbedTemplate

embed_template = EmbedTemplate(title="Private Matches", colour=discord.Colour.teal())


class MatchMakingRating(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(
        help="Checks the peak mmr for yourself or the user you specifiy.",
        brief="Checks a user's peak mmr.",
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def checkpeak(
        self,
        ctx: commands.Context,
        user: Option(discord.Member, "User", required=False),
    ):
        if ctx.channel.name != os.environ.get("6_MAN_CHANNEL"):
            return

        embed = embed_template.copy()

        sql = "SELECT mmr FROM player WHERE discord_id = ?"

        user_to_check = user or ctx.author

        result = database.field(sql, user_to_check.id)

        if result is None:
            embed.add_field(
                name="Match Making Rating!",
                value=f"{user_to_check.mention} has not set their MMR! Type `/setpeak <amount>` to set it.",
                inline=False,
            )
        else:
            embed.add_field(
                name="Match Making Rating!",
                value=f"{user_to_check.mention}: {str(result)}",
                inline=False,
            )

        await ctx.respond(embed=embed)

    @slash_command(
        help="Sets your peak mmr used for balancing in the private matches team-deciding methods.",
        brief="Sets your peak mmr.",
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def setpeak(
        self,
        ctx: commands.Context,
        mmr: Option(int, "MMR", required=True, min_value=100, max_value=2900),
    ):
        if ctx.channel.name != os.environ.get("6_MAN_CHANNEL"):
            return

        sql = "SELECT * FROM player WHERE discord_id = ?"
        user = database.record(sql, ctx.author.id)

        # if user is db, update
        if user is None:
            sql = "INSERT INTO player (discord_id, mmr) VALUES (?, ?)"
            database.execute(sql, ctx.author.id, mmr)
        # else, add user to db
        else:
            sql = "UPDATE player SET mmr = ? WHERE discord_id = ?"
            database.execute(sql, mmr, ctx.author.id)

        embed = embed_template.copy()

        embed.add_field(
            name="Match Making Rating!",
            value=f"{ctx.author.mention} set their mmr to: {str(mmr)}",
            inline=False,
        )

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(MatchMakingRating(bot))
