import discord
from discord.ext import commands
import json

with open("data.json", "r") as f:
    data = json.load(f)


def write_json(data):
    with open("data.json", "w") as f:
        json.dump(data, f)


general_names = data["general-names"]
custom_general_names = data["custom-general-names"]
requested_general_names = []


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="general-name", aliases=["gn"], brief="`!general-name <name>`. Used for changing the current general channel name.", help="`!general-name <name>`. Used for changing the current general channel name. Name can be anything, and is formatted as `general-namegiven`. Dev only command")
    @commands.has_permissions(manage_channels=True)
    async def general_name(self, ctx, name):
        channel = self.bot.get_channel(id=791102724027580486)
        new_name = "general-" + name
        await channel.edit(name=new_name)
        embed = discord.Embed(
            title=f":white_check_mark: Successfuly changed general name to {new_name}", color=discord.Color.green())
        await ctx.channel.send(embed=embed)

    @commands.command(name="request-general-name", aliases=["rgn"], brief="`!request-general-name [name]`. Used for requesting new general names.", help="`!request-general-name [name]`. Used for requesting new general names. Names have to be approved by a moderator before being approved.")
    async def request_general_name(self, ctx, name):
        requested_general_names.append(name)
        embed = discord.Embed(
            title=f":white_check_mark: Successfuly requested {name}", color=discord.Colour.green())
        await ctx.channel.send(embed=embed)

    @commands.command(name="approve-general-name", aliases=["agn", "argn"], brief="`!approve-general-name [name]`. Approves the passed general name.", help="`!approve-general-name [name]`. Approved the passed general name. Moderator only command.")
    @commands.has_permissions(ban_members=True)
    async def approve_general_name(self, ctx, name):
        if name in requested_general_names:
            data["custom-general-names"].append(name)
            write_json(data)
            requested_general_names.remove(name)
            embed = discord.Embed(
                title=f":white_check_mark: Successfuly approved requested general name {name}", color=discord.Colour.green())
        else:
            embed = discord.Embed(
                title=f":x: Name {name} not found", color=discord.Colour.red())
        await ctx.channel.send(embed=embed)

    @commands.command(name="display-requested-general-names", aliases=["display-requested-general-name", "drgn", "drg", "drn"], brief="`!display-requested-general-names`. Used to display the requested general naems.", help="`!display-requested-general-names`. Used to display the requested general names. Shows all the names users have requested that still need to be approved.")
    async def display_requested_general_names(self, ctx):
        if len(requested_general_names) == 0:
            embed = discord.Embed(title="Requested General Names",
                                  description="None", color=discord.Colour.blurple())
        else:
            embed = discord.Embed(title="Requested General Names", description=", ".join(
                requested_general_names), color=discord.Colour.blurple())
        await ctx.channel.send(embed=embed)

    @commands.command(name="clear-requested-general-names", aliases=["clear-general-names", "clear-requested-names", "crn", "crgn", "cgn"], brief="`!clear-requested-general-names`. Used for clearing all of the requested general names.", help="`!clear-requested-general-names`. Used for clearing all of the requested general names. All of the requested names that haven't been approved will be cleared. Moderator only command.")
    @commands.has_permissions(ban_members=True)
    async def clear_requested_general_names(self, ctx):
        requested_general_names.clear()
        await ctx.channel.send(":white_check_mark: Successfuly cleared all of the requested general names")

    @commands.command(name="clear-selected-general-name", aliases=["clear-selected-requested-name", "csrn", "csgn"], brief="`!clear-selected-general-name [name]`. Used for clearing a specified requested general name.", help="`!clear-selected-general-name [name]`. Used for clearing a specified requested general name. Finds and removes the specified requested general name. Moderator only command.")
    @commands.has_permissions(ban_members=True)
    async def clear_selected_general_name(self, ctx, name):
        if name in requested_general_names:
            requested_general_names.remove(name)
            embed = discord.Embed(
                title=f":white_check_mark: Successfuly removed name {name}", color=discord.Colour.green())
        else:
            embed = discord.Embed(
                title=f":x: Name {name} does not exist", color=discord.Colour.red())
        await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(GeneralCog(bot))
