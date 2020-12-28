import discord
from discord.ext import commands


class SlowmodeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set-slowmode", aliases=['slowmode', 'sm', 's-m'], brief="`!set-slowmode [interval]`. Used for changing the current slowmode in a channel.", help="`!set-slowmode [interval]`. Used for changing the slowmode in a current channel. This command changes the slowmode interval to a number that the user specifies. Moderator only command.")
    @commands.has_permissions(ban_members=True)
    async def set_slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(
            title=f":white_check_mark: Slowmode for the current channel successfully set to {seconds}",  color=discord.Colour.green())
        await ctx.channel.send(embed=embed)

    @commands.command(name="reset-slowmode", aliases=["rs"], brief="`!reset-slowmode`. Used for resetting the current slowmode in a channel to zero.", help='`!reset-slowmode`, Used for resetting the current slowmode in a channel to zero. This command can be used to reset a slowmode specified by `!set-slowmode`. Moderator only command.')
    @commands.has_permissions(ban_members=True)
    async def reset_slowmode(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        embed = discord.Embed(
            title=":white_check_mark: Slowmode for the current channel has successfully been reset",  color=discord.Colour.green())
        await ctx.channel.send(embed=embed)

    @commands.command(name="get-slowmode", aliases=["gsm", "gs"], brief="`!get-slowmode`. Used for retrieving the set slowmode in a channel.", help="`!get-slowmode`. Used for retrieving the set slowmode in a channel.")
    @commands.has_permissions(ban_members=True)
    async def get_slowmode(self, ctx):
        current_slowmode = ctx.channel.slowmode_delay
        await ctx.channel.send(f"Slowmode for current channel is {current_slowmode}")


def setup(bot):
    bot.add_cog(SlowmodeCog(bot))
