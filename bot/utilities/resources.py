import discord
from discord.ext import commands

cogs = ("ResourcesCog", "ModerationCog", "SilencerCog", "SlowmodeCog", "PollCog")


class ResourcesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", brief="`!help <command/cog/section>`. Used to display the help message for the given argument.", help="`!help <command/cog/section>`. Used to display the help message for the given argument. If no arguments are specified, then the default help page will be shown.")
    async def help(self, ctx, argument=None):
        if argument is None:
            embed = discord.Embed(
                title=':grey_question: Help', description="Default help page. Use `!help [command]` for specific information on a command, use !help [cog] for information on a cog, or use !help [section] for information on a section.", color=discord.Colour.orange())
            embed.add_field(
                name="Cogs", value="Cogs are a group of commands that are grouped together based on subject. Use `!help [cog]` for more information on a cog and its commands.", inline=False)
            embed.add_field(
                name="Help", value="Use `!help` to view this page. You can do `!help [cog]` for information on a cog, or `!help [section]` for information on a specific section.", inline=False)
            embed.add_field(
                name="Features", value="Use `!help features` to view information on all of the features and things that this bot automates.", inline=False)
            embed.add_field(
                name="Roles", value="You can head over to the #roles channel to claim your roles. Claiming these roles is optional. There are roles for pings, and roles used to classify you.", inline=False)
            embed.add_field(
                name="Rules", value="Make sure to check #rules when you first join, and make sure to abide by the rules. Each member of staff has the authority to punish you how they deem fit if you break the rules. If you have any moderation related concerns, contact the moderators. Use !rule [rule_num] to view information on a rule.", inline=False)
        elif argument.lower() in ("cog", "cogs"):
            embed = discord.Embed(title=":grey_question: Help: Cogs",
                                  description="The help message for all of the bots cogs. Use !help [command] to get help on a specific command, or do !help to view the default help page.", color=discord.Colour.blue())
            embed.add_field(
                name="Moderation", value='Use !help moderation to view details on the Moderation cog. This cog includes commands for server moderation, such as ban and mute commands', inline=False)
            embed.add_field(
                name="Silence", value="Use !help silence to view details on the Silence cog. This cog has detailed information on the !silence command.", inline=False)
            embed.add_field(
                name="Slowmode", value="Use !help slowmode to view details on the Slowmode cog. This cog has detailed information on the !slowmode command.", inline=False)
            embed.add_field(
                name="Poll", value="Use !help poll to view information on the Slowmode cog. This cog has information on the !poll command.", inline=False)
            embed.add_field(
                name="Server", value='Use !help server to view information on the Server cog. This cog has commands that are used to edit the server.', inline=False)
            embed.add_field(name="Utils", value="Use !help utils to view information on the Utils cog. This cog has utility commands that can be used to view information and perform other small tasks.", inline=False)
            embed.add_field(
                name="Resources", value="Use !help resources to view information on the Resources cog. This cog includes commands that are used to view server resources, such as !help.", inline=False)
            embed.set_footer(
                text=f"!help [command] for specific information on a single command. !help [cog] for information on a cog. !help [section] for information on a section")
        elif argument.lower() in ("moderation", "mods", "moderators", "moderator"):
            embed = discord.Embed(title=":grey_question: Help: Moderation",
                                  description="The help message on the moderation cog. Use !help [command] for specific information on a command.", color=discord.Colour.purple())
            for i in self.bot.get_cog("ModerationCog").get_commands():
                if not i.hidden:
                    embed.add_field(name=i.name, value=i.brief, inline=False)
        elif argument.lower() in ("silence", "silencing"):
            embed = discord.Embed(title=":grey_question: Help: Silence",
                                  description="The help message on the silence cog. Use !help [command] for specific information on a command.", color=discord.Colour.purple())
            for i in self.bot.get_cog("SilencerCog").get_commands():
                if not i.hidden:
                    embed.add_field(name=i.name, value=i.brief, inline=False)
        elif argument.lower() in ("slowmode", "sm", "slowmodes"):
            embed = discord.Embed(title=":grey_question: Help: Slowmode",
                                  description="The help message on the slowmode cog. Use !help [command] for specific information on a command.", color=discord.Colour.purple())
            for i in self.bot.get_cog("SlowmodeCog").get_commands():
                if not i.hidden:
                    embed.add_field(name=i.name, value=i.brief, inline=False)
        elif argument.lower() in ("poll", "polls"):
            embed = discord.Embed(title=":grey_question: Help: Poll",
                                  description="The help message on the poll cog. Use !help [command] for specific information on a command.", color=discord.Colour.purple())
            for i in self.bot.get_cog("PollCog").get_commands():
                if not i.hidden:
                    embed.add_field(name=i.name, value=i.brief, inline=False)
        elif argument.lower() in ("server", "servers"):
            embed = discord.Embed(title=":grey_question: Help: Server",
                                  description="The help message on the server cog. Use !help [command] for specific information on a command.", color=discord.Colour.purple())
            for i in self.bot.get_cog("ServerConfigCog").get_commands():
                if not i.hidden:
                    embed.add_field(name=i.name, value=i.brief, inline=False)
        elif argument.lower() in ("utils", "utilities", "util"):
            embed = discord.Embed(title=":grey_question: Help: Utils",
                                  description="The help message on the utils cog. Use !help [command] for specific information on a command.", color=discord.Colour.purple())
            for i in self.bot.get_cog("UtilsCog").get_commands():
                if not i.hidden:
                    embed.add_field(name=i.name, value=i.brief, inline=False)
        elif argument.lower() in ("resources", "resource"):
            embed = discord.Embed(title=":grey_question: Help: Resources",
                                  description="The help message on the resources cog. Use !help [command] for specific information on a command.", color=discord.Colour.purple())
            for i in self.bot.get_cog("ResourcesCog").get_commands():
                if not i.hidden:
                    embed.add_field(name=i.name, value=i.brief, inline=False)
        else:
            found = False
            for i in self.bot.cogs:
                for command in self.bot.get_cog(i).get_commands():
                    if str(argument) == str(command):
                        embed = discord.Embed(title=f":grey_question: Help: {command}", description=command.help, color=discord.Colour.blue())
                        found = True
                        break
                    else:
                        print(command)
            if not found:
                embed = discord.Embed(title=f":x: No help found on command {argument}", color=discord.Colour.red())
            

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ResourcesCog(bot))
