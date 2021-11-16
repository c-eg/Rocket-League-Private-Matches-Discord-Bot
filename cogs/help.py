# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

embed_template = discord.Embed(
    title='Private Matches',
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
    async def help(self, ctx: commands.Context):
        embed = embed_template.copy()

        help_string = "Here is a list of commands that you can use.\narguments: <argument> are required, [argument] are optional\n\n"

        help_string += "`;setpeak <mmr>` to set your highest mmr\n"
        help_string += "`;cheapeak [user]` check your peak mmr or another user's peak mmr\n"
        help_string += "`;queue` join the queue\n"
        help_string += "`;leave` leave the queue\n"
        help_string += "`list` list all users in queue\n"
        help_string += "`;clear` (ADMIN ONLY) clear the queue\n"
        help_string += "`;help` prints this message :)"

        embed.add_field(
            name='Commands!',
            value=help_string,
            inline=False
        )

        await ctx.channel.send(embed=embed)
