# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

from db import database

embed_template = discord.Embed(
    title='Private Matches',
    colour=discord.Colour.teal()
)
embed_template.set_footer(
    text='UEA Private Matches by curpha',
    icon_url='https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars/be/bed810f8bebd7be235b8f7176e3870de1006a6e5_full.jpg'
)


class MatchMakingRating(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def checkpeak(self, ctx: commands.Context, user: discord.Member = None):
        if ctx.channel.name != '6-mans-test-things':
            return

        embed = embed_template.copy()

        sql = 'SELECT mmr FROM player WHERE discord_id = ?'

        if user:
            user_to_check = user
        else:
            user_to_check = ctx.author

        result = database.field(sql, user_to_check.id)

        if result is None:
            embed.add_field(
                name='Match Making Rating!',
                value=user_to_check.mention + ' has not set their MMR! Type `;setpeak <amount>` to set it.',
                inline=False
            )
        else:
            embed.add_field(
                name='Match Making Rating!',
                value=user_to_check.mention + ': ' + str(result),
                inline=False
            )

        await ctx.channel.send(embed=embed)

    @checkpeak.error
    async def checkpeak_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.channel.send("Please enter a valid user!")
            return
        else:
            raise error

    @commands.command()
    async def setpeak(self, ctx: commands.Context, mmr):
        if ctx.channel.name != '6-mans-test-things':
            return

        if not mmr:
            await ctx.channel.send("Please enter an mmr!")
            return

        try:
            mmr = int(mmr)
        except:
            await ctx.channel.send("Please enter a valid mmr!")
            return

        if not 1 <= mmr <= 3000:
            await ctx.channel.send("Please enter a valid mmr!")
            return

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
