import discord
from discord.ext import commands

cogs = ("ResourcesCog", "ModerationCog",
        "SilencerCog", "SlowmodeCog", "PollCog")


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
        elif argument.lower() in ("help"):
            embed = discord.Embed(title=":grey_question: Help",
                                  description="The help page for the Help section of the bot", color=discord.Colour.teal())
            embed.add_field(
                name="Getting Help", value="You can get help on something using the `!help` command, and navigating around its options. Feel free to DM the staff if you need anything.")
        elif argument.lower() in ("features", "feature"):
            embed = discord.Embed(title=":grey_question: Features",
                                  description="The help message for the Features section of the bot.", color=discord.Colour.dark_green())
            embed.add_field(name="Changing General Name", value="The servers general name changes every 24 hours, these names are formatted as `general-whatevername`. The names switch between inside jokes and precious metals. You can learn more about this by doing `!help general`.", inline=False)
            embed.add_field(
                name="Reaction Roles", value="In the #roles channel in the server, you can react to messages left by carl bot in order to claim yourself roles.", inline=False)
        elif argument.lower() in ("roles", "role"):
            embed = discord.Embed(title=":grey_question: Roles",
                                  description="The help message for the Roles section of the bot. All of the roles are listed from high to low in terms of ranking.", color=discord.Colour.dark_blue())
            embed.add_field(name="Admin", value="Admin is the highest role in the server. Members with this role have administrator privilages and manage and moderate the server. The admins enforce the rules and manage the server.", inline=True)
            embed.add_field(name="Moderator", value="Moderators are the rule enforcers of the server. Members who have this role have perms to mute/ban people, as well as silence channels. Moderators are allowed to punish people who don't follow the rules however they deem fit.", inline=True)
            embed.add_field(name="Dev", value="Devs manage the server. The main job of a Dev is to manage and keep in track of the server. Devs have permissions to edit the server and delete and make channels and categories.", inline=True)
            embed.add_field(name="Software Dev", value="Software Devs are members that partake in the development of the Infinite Spammers Bot, as well as other projects. Members who have this role don't get any extra permissions, but are considered staff.", inline=True)
            embed.add_field(name="Newsletter", value="People with the Newsletter role are members that help out with the Infinite Spammers Newsletter. They don't have any extra permissions, but are considered staff.", inline=True)
            embed.add_field(name="Citizen", value="Citizen is the default role that is given to new members that join the server. People with this role have default permissions, and includes the majority of the servers members.", inline=True)
            embed.add_field(
                name="Pronouns", value="The server has three pronoun roles you can claim in #roles. He/Him, She/Her, and They/Them. Claiming these roles is strictly optional.", inline=True)
            embed.add_field(name="Location", value="The server has several location roles you can claim in #roles. North America, South America, Asia, Europe, Africa and Australia. Claiming these roles is strictly optional.", inline=True)
            embed.add_field(
                name="Age", value="The server has two age roles. <18 and >18. Claiming these roles is strictly optional.", inline=True)
            embed.add_field(
                name="Crewmates", value="The Crewmates role is a pinging role that people can claim if they want to be pinged for playing Among Us.", inline=True)
            embed.add_field(
                name="Game Night", value="The Game Night role is a pinging role that people can claim if they want to be pinged for any game nights.", inline=True)
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
                        embed = discord.Embed(
                            title=f":grey_question: Help: {command}", description=command.help, color=discord.Colour.blue())
                        found = True
                        break
                    else:
                        print(command)
            if not found:
                embed = discord.Embed(
                    title=f":x: No help found on command {argument}", color=discord.Colour.red())

        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["git", "source"], brief="`!github`. Used for displaying the link to the bots github.", help="`!github`. Used for displaying the link to the bots github.")
    async def github(self, ctx):
        embed = discord.Embed(title="Infinite Spammers Bot Source Code",
                              description="https://github.com/AbooMinister25/InfiniteSpammersBot")
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ResourcesCog(bot))
