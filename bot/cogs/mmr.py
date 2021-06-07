import discord
from discord.ext import commands

from bot.db import database
from bot.models.player import Player

queue_message = discord.Embed(
    title='Private Matches',
    colour=discord.Colour.dark_red()
)
queue_message.set_footer(
    text='Rocket League Private Matches Discord Bot',
    icon_url='https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/avatars/59/595a3684e667dc05e9d0d7e76efa8bb33b43a45f_full.jpg'
)


class MatchMakingRating(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def mmr(self, ctx: commands.Context):
        discord_id = ctx.author.id
        player = None

        # TODO: Make work when a user is passed as an argument,
        #  checking the passed user's mmr

        try:
            player = self.bot.get_cog('Servers').get_player(discord_id)
        except KeyError:
            pass

        message = queue_message.copy()

        if player is None:
            message.add_field(
                name='Match Making Rating!',
                value=ctx.author.mention + ' has not set their MMR! Type `;setmmr <amount>` to set it.',
                inline=False
            )
        else:
            message.add_field(
                name='Match Making Rating!',
                value=ctx.author.mention + ': ' + str(player.get_mmr()),
                inline=False
            )

        await ctx.channel.send(embed=message)

    @commands.command()
    async def setmmr(self, ctx: commands.Context, mmr: int):
        # TODO: Watch video on autosaving database.db
        #  might have to change this to update the player dictionary to then be autosaved by the scheduler

        s = self.bot.get_cog('Servers')
        p = None

        try:
            p = s.get_player(ctx.author.id)
        except KeyError:
            pass

        if p is None:
            s.add_player(Player(discord_id=ctx.author.id, mmr=mmr))
            sql = 'INSERT INTO player (discord_id, mmr) VALUES (?, ?)'
            database.execute(sql, ctx.author.id, mmr)
        else:
            sql = 'UPDATE player SET mmr = ? WHERE discord_id = ?'
            database.execute(sql, mmr, ctx.author.id)

        database.commit()

def setup(bot):
    bot.add_cog(MatchMakingRating(bot))




