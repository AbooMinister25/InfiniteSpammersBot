import discord
from discord.ext import commands
import traceback


class ErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandNotFound)

        if isinstance(error, ignored):
            return
        if isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(
                title=f":x: Command {ctx.command} has been disabled", color=discord.Colour.red())
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title=f":x: Invalid member given", color=discord.Colour.red())
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title=f":x: You are not authorized to use this command", color=discord.Colour.red())
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title=f":x: Please enter the correct number of arguments for this command", color=discord.Colour.red())
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                title=f":x: Specified member could not be found", color=discord.Colour.red())

        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(ErrorCog(bot))
