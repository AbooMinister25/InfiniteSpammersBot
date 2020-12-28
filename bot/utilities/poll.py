import discord
from discord.ext import commands


class PollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["make-poll", "mp"], brief="`!poll [title] <description> [*emojis]`. Used for creating a poll in the current channel.", help="`!poll [title] <description> [*emojis]`. Used for creating a poll in the current channel. Users can react to this poll and can be used to tally votes or measure participation in an event.")
    async def poll(self, ctx, title, description=None, *emojis):
        if len(title) > 256:
            embed = discord.Embed(title=":x: The title cannot be longer than 256 characters", color=discord.Colour.red())
        if len(emojis) < 2:
            embed = discord.Embed(title=":x: You have to provide at least two reactions", color=discord.Colour.red())
        if len(emojis) > 20:
            embed = discord.Embed(title=":x: You cannot have more than 20 emojis", color=discord.Colour.red())
        if description is not None:
            embed = discord.Embed(title=title, description=description, color=discord.Colour.orange())
        else:
            embed = discord.Embed(title=title, color=discord.Colour.magenta())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        message = await ctx.channel.send(embed=embed)
        for reaction in emojis:
            await message.add_reaction(reaction)


def setup(bot):
    bot.add_cog(PollCog(bot))