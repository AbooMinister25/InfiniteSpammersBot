import discord
from discord.ext import commands
from discord.utils import get


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="`!ban [member] <reason>`. Used for banning a user from the server.", help="`!ban [member] <reason>`. Used to banning a user from the server, the user cannot rejoin the server unless unbanned. Moderator only command.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, *, member: discord.Member, ban_message="A Moderator decided you were violating the community guidelines"):
        message = f"You have been banned from {ctx.guild.name} because {ban_message}"
        try:
            await member.send(message)
        except:
            pass
        await ctx.guild.ban(member, reason=ban_message)
        embed = discord.Embed(
            title=f":white_check_mark: User {member} was successfully banned by {ctx.messsage.author}", color=discord.Colour.green())
        await ctx.channel.send(embed=embed)

    @commands.command(brief="`!unban [member]`. Used for unbanning a user from the server.", help="`!unban [member]`. Used for unbanning a banned user from the server, allowing them to rejoin. Moderator only command.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild_bans()
        member_name, member_discriminator = member.split("#")
        if banned_users is None:
            embed = discord.Embed(
                title=":x: There are no banned users",  color=discord.Colour.red())
            await ctx.channel.send(embed=embed)
            return
        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.member_discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(
                title=f":white_check_mark: Welcome back, {user}, you have been successfully unbanned by {ctx.message.author}",  color=discord.Colour.green())
            await ctx.channel.send(embed=embed)
            return
        else:
            embed = discord.Embed(
                title=f":x: Failed to unban user {user}",  color=discord.Colour.red)
            await ctx.channel.send(embed=embed)
            return

    @commands.command(brief="`!mute [member]`. Used for muting a member in the server.", help="`!mute [member]`. Used for muting a member in the server. This command adds the `Muted` role to the passed user, which makes then unable to talk in text channels and unable to speak in voice channels. Moderator only command.")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        user = ctx.author
        role = get(user.guild.roles, name="muted")
        await member.add_roles(role)
        embed = discord.Embed(
            title=f":white_check_mark: User {member} was successfully muted by {ctx.author}",  color=discord.Colour.green())
        await ctx.channel.send(embed=embed)

    @commands.command(brief="`!unmute [member]`. Used for unmuting a member in the server.")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        user = ctx.message.author
        role = get(user.guild.roles, name="muted")
        try:
            await member.remove_roles(role)
            embed = discord.Embed(
                title=f":white_check_mark: Successfully unmuted {member}",  color=discord.Colour.green())
        except:
            embed = discord.Embed(
                title=f":x: Failed to unmute user {member}",  color=discord.Colour.red())
        await ctx.channel.send(embed=embed)

    @commands.command(brief="`!warn [member]`. Used for warning a user for committing an infraction.", help="`!warn [member]`. Used for warning a user for committing an infraction. This can be used when a moderator wants to tell a user to stop commiting an infraction, without muting or banning. Moderator only command.")
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member):
        message = f":white_check_mark: {ctx.message.author} warned {member}. {' '.join(message)}"
        await ctx.channel.send(message)


def setup(bot):
    bot.add_cog(ModerationCog(bot))
