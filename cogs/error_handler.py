

from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """
        Global error handler.
        """
        prefix = await self.bot.get_prefix(ctx.message)

        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"{ctx.command} is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = f"You are missing the required permissions to use {ctx.command}"
        elif isinstance(error, commands.UserInputError):
            message = f"Invalid input! Please use `{prefix}help {ctx.command}` for help."
        else:
            message = "Oh no! Something went wrong while running the command!"
            print(error)

        await ctx.channel.send(message, delete_after=30)


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
