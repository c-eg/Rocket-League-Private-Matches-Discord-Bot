import discord
from discord.ext import commands

from bot.db import database

queue_message = discord.Embed(
    title='Private Matches',
    colour=discord.Colour.dark_red()
)
queue_message.set_footer(
    text='Rocket League Private Matches Discord Bot',
    icon_url='https://cdn.cloudflare.steamstatic.com/steamcommunity/public/imag'
             'es/avatars/59/595a3684e667dc05e9d0d7e76efa8bb33b43a45f_full.jpg'
)


class MatchMakingRating(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def mmr(self, ctx: commands.Context, user=None):
        user_to_check = ctx.author

        if user is not None:
            user_to_check = await self.bot.fetch_user(user[3:-1])

        message = queue_message.copy()

        sql = 'SELECT mmr FROM player WHERE discord_id = ?'
        result = database.field(sql, user_to_check.id)

        if result is None:
            message.add_field(
                name='Match Making Rating!',
                value=user_to_check.mention + ' has not set their MMR! Type '
                                              '`;setmmr <amount>` to set it.',
                inline=False
            )
        else:
            message.add_field(
                name='Match Making Rating!',
                value=user_to_check.mention + ': ' + str(result),
                inline=False
            )

        await ctx.channel.send(embed=message)

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


def setup(bot):
    bot.add_cog(MatchMakingRating(bot))
