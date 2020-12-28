import discord
from discord.ext import commands, tasks
import asyncio


def parse_duration(duration):
    chars_list = duration.strip()
    if "s" in chars_list:
        duration_type = "seconds"
    elif "m" in chars_list:
        duration_type = "minutes"
    else:
        return "Invalid Duration"

    if duration_type == "seconds":
        return dict({"duration_type": "seconds", "duration": duration.strip("s")})
    elif duration_type == "minutes":
        return dict({"duration_type": "minutes", "duration": int(duration.strip("m")) * 60})


class SilencerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["hush", "shut", "shutup", "quiet", "shutupplsguys"], brief="`!silence <duration>`. Used for silencing the current channel for an optional duration.", help="!silence <duration>. Used for silencing the current channel for an optional duration. Silencing a channel prevents all non moderators from speaking in the channel, and can be used to stop chaotic conversations. Moderator only command.")
    @commands.has_permissions(ban_members=True)
    async def silence(self, ctx, duration=None):
        if ctx.channel.id == "718882685124214825":
            embed = discord.Embed(
                title=":x: Can't silence in staff channels",  color=discord.Colour.red())
        else:
            if duration is None:
                await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
                embed = discord.Embed(
                    title=":white_check_mark: Succesfully silenced current channel",  color=discord.Colour.green())
                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
                parsed_duration = parse_duration(duration)
                if parsed_duration == "Invalid Duration":
                    embed = discord.Embed(
                        title=f":x: Invalid duration {duration} given", color=discord.Colour.red())
                    await ctx.channel.send(embed=embed)
                    return
                duration_type = parsed_duration["duration_type"]
                duration = parsed_duration["duration"]
                embed = discord.Embed(
                    title=f":white_check_mark: Succesfully silenced current channel for {duration} {duration_type}",  color=discord.Colour.green())
                await ctx.channel.send(embed=embed)
                await asyncio.sleep(duration)
                await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

    @commands.command(aliases=["unhush", "us", "unshut"], brief="`!unsilence`. Used for unsilencing the current channel.", help="`!unsilence`. Used for unsilencing the current channel. This allows all members to freely talk again.")
    @commands.has_permissions(ban_members=True)
    async def unsilence(self, ctx):
        if ctx.channel.id == "718882685124214825":
            embed = discord.Embed(
                title=":x: Can't silence in staff channels",  color=discord.Colour.red())
        else:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            embed = discord.Embed(
                title=":white_check_mark: Succesfully unsilenced current channel",  color=discord.Colour.green())
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(SilencerCog(bot))
