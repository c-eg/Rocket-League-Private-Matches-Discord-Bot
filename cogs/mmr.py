# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

from db import database

embed_template = discord.Embed(
    title='UEA Private Matches',
    colour=discord.Colour.dark_red()
)
embed_template.set_footer(
    text='UEA Private Matches by curpha',
    icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars/be/bed810f8bebd7be235b8f7176e3870de1006a6e5_full.jpg'
)


class MatchMakingRating(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def mmr(self, ctx: commands.Context):
        embed = embed_template.copy()

        sql = 'SELECT mmr FROM player WHERE discord_id = ?'
        result = database.field(sql, ctx.author.id)

        if result is None:
            embed.add_field(
                name='Match Making Rating!',
                value=ctx.author.mention + ' has not set their MMR! Type `;setmmr <amount>` to set it.',
                inline=False
            )
        else:
            embed.add_field(
                name='Match Making Rating!',
                value=ctx.author.mention + ': ' + str(result),
                inline=False
            )

        await ctx.channel.send(embed=embed)

    @commands.command()
    async def setmmr(self, ctx: commands.Context, mmr: int):
        sql = 'SELECT * FROM player WHERE discord_id = ?'
        user = database.record(sql, ctx.author.id)

        # if user is db, update
        if user is None:
            sql = 'INSERT INTO player (discord_id, mmr) VALUES (?, ?)'
            database.execute(sql, ctx.author.id, mmr)
        # else, add user to db
        else:
            sql = 'UPDATE player SET mmr = ? WHERE discord_id = ?'
            database.execute(sql, mmr, ctx.author.id)

        embed = embed_template.copy()

        embed.add_field(
            name='Match Making Rating!',
            value=f"{ctx.author.mention} set their mmr to: {str(mmr)}",
            inline=False
        )

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MatchMakingRating(bot))
