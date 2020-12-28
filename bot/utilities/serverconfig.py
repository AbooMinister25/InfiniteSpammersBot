import discord
from discord.ext import commands
from discord.utils import get


class ServerConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create-channel", aliases=["cc", "new-channel"], brief="`!create-channel [name]`. Used for creating a new channel.", help="`!create-channel [name]`. Used for creating a new channel. The channel will be a text channel. Dev only command")
    @commands.has_permissions(manage_channels=True)
    async def create_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            await guild.create_text_channel(channel_name)
            embed = discord.Embed(
                title=f":white_check_mark: Channel {channel_name} successfully created", color=discord.Colour.green())
        else:
            embed = discord.Embed(
                title=f":x: Channel {channel_name} already exists", color=discord.Colour.red())
        await ctx.channel.send(embed=embed)

    @commands.command(name="rename-channel", brief="`!rename-channel [channel] [name]`. Used for renaming a specified channel to a specified name.", help="`!rename-channel [channel] [name]`. Used for renaming a specified channel to a specified name. The name can be whatever the user specifies. Dev only command.")
    @commands.has_permissions(manage_channels=True)
    async def rename_channel(self, ctx, channel: discord.TextChannel, *, newName):
        embed = discord.Embed(
            title=f":white_check_mark: Successfully renamed channel {channel} to {newName}", color=discord.Colour.green())
        await ctx.channel.send(embed=embed)

    @commands.command(name="delete-channel", aliases=["dc"], brief="`!delete-channel [channel]`. Used for deleting a specific text channel.", help="`!delete-channel [channel]`. Used for deleting a specific text channel from the server. The channel can only be a text channel. Dev only command.")
    @commands.has_permissions(manage_channels=True)
    async def delete_channel(self, ctx, channel_name):
        guild = ctx.guild
        channel = discord.utils.get(guild.channels, name=channel_name)
        if channel is not None:
            await channel.delete()
            embed = discord.Embed(
                title=f":white_check_mark: Channel {channel_name} successfully deleted", color=discord.Colour.green())
        else:
            embed = discord.Embed(
                title=f":x: No channel named {channel_name}", color=discord.Colour.red())
        await ctx.channel.send(embed=embed)

    @commands.command(name="create-category", aliases=["cca", "ccat", "new-category"], brief="`!create-category [category-name]`. Used for creating a new category in the server.", help="`!create-category [category-name]`. Used for creating a new category in the server with a specified name. Dev only commmand." )
    @commands.has_permissions(manage_channels=True)
    async def create_category(self, ctx, *, category_name):
        guild = ctx.guild
        await guild.create_category(category_name)
        embed = discord.Embed(
            title=f":white_check_mark: Category {category_name} successfully created", color=discord.Colour.green())
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ServerConfigCog(bot))
