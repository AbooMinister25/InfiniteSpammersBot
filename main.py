from discord.ext import commands, tasks
from discord.utils import get
import discord
import json
import random as rd
import wikipedia
from PyDictionary import PyDictionary
from newsapi import NewsApiClient
import subprocess
import os


token = open('token.txt').read()
bot = commands.Bot(command_prefix="!", help_message="help")
client = discord.Client
bot.remove_command("help")


with open("data.json", "r") as f:
    data = json.load(f)


def write_json(data):
    with open("Infinite Spammers Bot/data.json", "w") as f:
        json.dump(data, f)


generalNames = data["general-names"]
customGeneralNames = data["custom-general-names"]
topics = data["topics"]
requestedGeneralNames = []
requestedTopics = []


dictionary = PyDictionary()
newsapi = NewsApiClient(api_key='7458c5de548342898784767cecc360a7')


@bot.command(name="create-channel", help="Admin command for creating channel. Example: !create-channel (channel name)")
@commands.has_any_role("Admin", "Dev")
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if channel_name == None:
        await ctx.send("Please enter the channel name")
    if not existing_channel:
        print('Creating new channel ' + channel_name)
        await guild.create_text_channel(channel_name)
        await ctx.send("Creating new channel " + channel_name)
    else:
        await ctx.send("Channel already exists")


@bot.command(name="ban", help="Admin command for banning a user with an optional ban message. Example: !ban (user) (optional ban meessage)")
@commands.has_any_role("Admin", "Moderator")
async def ban(ctx, *, member: discord.Member, ban_message="An Admin decided you were violating the community guidelines"):
    message = f"You have been banned from {ctx.guild.name} because {ban_message}"
    try:
        await member.send(message)
    except:
        pass
    await ctx.guild.ban(member, reason=ban_message)
    await ctx.channel.send(f"{member} was banned")


@bot.command(name="unban")
@commands.has_any_role("Admin", "Moderator")
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@bot.command(name="tempban")
@commands.has_any_role("Admin", "Moderator")
async def tempban(ctx, *, member: discord.Member, time, ban_message="An admin decided you were violating the community guidelines"):
    message = f"You have been banned from {ctx.guild.name} because {ban_message} for {time}"
    try:
        await member.send(message)
    except:
        pass
    await ctx.guild.ban(member, reason=ban_message)
    await ctx.channel.send(f"{member} was banned")


@bot.command(name="mute", help="Admin command for muting a user")
@commands.has_any_role("Admin", "Moderator")
async def mute(ctx, member: discord.Member):
    user = ctx.message.author
    role = get(user.guild.roles, name="muted")
    await member.add_roles(role)
    await ctx.channel.send(f"{ctx.message.author} has muted {member}")


@bot.command(name="unmute", help="Admin command for unmuting a muted user")
@commands.has_any_role("Admin", "Moderator")
async def unmute(ctx, member: discord.Member):
    user = ctx.message.author
    role = get(user.guild.roles, name="muted")
    await member.remove_roles(role)
    await ctx.channel.send(f"{ctx.message.author} has unmuted {member}")


@bot.command(name="def", help="Command for finding the definition of the given word")
async def define(ctx, word: str):
    try:
        result = dictionary.meaning(word)
        await ctx.channel.send("Here is the result of your query:\n" + str(result))
    except:
        await ctx.channel.send("Sorry, I couldn't find a definition for the given word")


@bot.command(name="poll", help="Command for creating polls, make sure to surround the text of the poll in double quotes")
async def poll(ctx, title, *emojis):
    if len(title) > 256:
        await ctx.channel.send(commands.BadArgument("The title cannot be longer than 256 characters"))
        return
    if len(emojis) < 2:
        await ctx.channel.send(commands.BadArgument("Please provide at least two reactions"))
        return
    if len(emojis) > 20:
        await ctx.channel.send(commands.BadArgument("You cannot have more than 20 options"))
        return
    embed = discord.Embed(title=title)
    message = await ctx.send(embed=embed)
    for reaction in emojis:
        await message.add_reaction(reaction)


@bot.command(name="site", help="Command for getting the link to our website")
async def site(ctx):
    embed = discord.Embed(title="https://infinitespammers.netlify.app")
    await ctx.channel.send(embed=embed)


@bot.command(name="rename-channel", help="Admin command for renaming channels")
@commands.has_any_role("Admin", "Dev")
async def renameChannel(ctx, channel: discord.TextChannel, *, newName):
    await channel.edit(name=newName)


@bot.command(name="github", help="gives the link for this bots github page")
async def github(ctx):
    embed = discord.Embed(
        title="https://github.com/AbooMinister25/InfiniteSpammersBot/blob/master/main.py")
    await ctx.channel.send(embed=embed)


@bot.command(name="pronoun", help="Command for settings pronouns")
async def pronoun(ctx, pronoun):
    member = ctx.message.author
    if pronoun == "he/him":
        role = get(member.guild.roles, name="He/Him")
        await member.add_roles(role)
    elif pronoun == "she/her":
        role = get(member.guild.roles, name="She/Her")
        await member.add_roles(role)
    elif pronoun == "they/them":
        role = get(member.guild.roles, name="They/Them")
        await member.add_roles(role)
    await ctx.channel.send("Pronoun Successfuly added")


@bot.command(name="rgn", help="Command for requesting names for the #general channel")
async def request_general_name(ctx, name):
    requestedGeneralNames.append(name)
    await ctx.channel.send("Name successfuly requested")


@bot.command(name="request-general-name", help="Command for requesting names for the #general channel")
async def request_general_name(ctx, name):
    requestedGeneralNames.append(name)
    await ctx.channel.send("Name successfuly requested")


@bot.command(name="display-requested-general-names", help="Command for displaying requested general names")
async def display_requested_general_names(ctx):
    await ctx.channel.send(f"Requested names: \n{requestedGeneralNames}")


@bot.command(name="drgn", help="Command for displaying requested general names")
async def display_requested_general_names(ctx):
    await ctx.channel.send(f"Requested names: \n{requestedGeneralNames}")


@bot.command(name="approve-requested-general-name", help="Command for approving requested general names")
@commands.has_role("Admin")
async def approve_requested_general_name(ctx, name):
    if name in requestedGeneralNames:
        customGeneralNames.append(name)
        with open("data.json", 'r') as f:
            write_json(data)
        await ctx.channel.send("Name approved")
    else:
        await ctx.channel.send("The requested name could not be found")


@bot.command(name="argn", help="Command for approving requested general names")
@commands.has_role("Admin")
async def approve_requested_general_name(ctx, name):
    if name in requestedGeneralNames:
        customGeneralNames.append(name)
        with open("data.json", 'r') as f:
            write_json(data)
        await ctx.channel.send("Name approved")
    else:
        await ctx.channel.send("The requested name could not be found")


@bot.command(name="clear-requested-general-names", help="Command for clearing requested general names")
@commands.has_role("Admin")
async def clear_requested_general_names(ctx):
    requestedGeneralNames.clear()


@bot.command(name="crgn", help="Command for clearing requested general names")
@commands.has_role("Admin")
async def clear_requested_general_names(ctx):
    requestedGeneralNames.clear()


@bot.command(name="clear-selected-general-name", help="Command for clearing a name from requested general names")
@commands.has_role("Admin")
async def clear_selected_general_name(ctx, name):
    try:
        requestedGeneralNames.remove(name)
        await ctx.channel.send("Name removed successfuly")
    except Exception as e:
        await ctx.channel.send(f"There was the following error while removing the given name: {e}")


@bot.command(name="silence", help="Command for silencing the current channel")
@commands.has_any_role("Admin", "Moderator")
async def silence(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.channel.send("Channel successfuly silenced")


@bot.command(name="unsilence", help="Command for unsilencing the current channel")
@commands.has_any_role("Admin", "Moderator")
async def unsilence(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.channel.send("Channel successfuly unsilenced")


@bot.command(name="rule", help="Command for displaying a given rule")
async def rule(ctx, rule):
    rule = int(rule)
    if rule == 1:
        embed = discord.Embed(
            title="No mass mentions such as @ everyone and @ here")
        await ctx.channel.send(embed=embed)
    elif rule == 2:
        embed = discord.Embed(title="No pinging the Admins unless necesarry")
        await ctx.channel.send(embed=embed)
    elif rule == 3:
        embed = discord.Embed(
            title="Absolutely no hate speech, homophobia, sexism, racism, or otherwise degrading comments")
        await ctx.channel.send(embed=embed)
    elif rule == 4:
        embed = discord.Embed(
            title="No NSFW content, please keep this place friendly for everyone")
        await ctx.channel.send(embed=embed)
    elif rule == 5:
        embed = discord.Embed(title="No innapropriate language and slurs")
        await ctx.channel.send(embed=embed)
    elif rule == 6:
        embed = discord.Embed(title="No unecessary spamming")
        await ctx.channel.send(embed=embed)
    elif rule == 7:
        embed = discord.Embed(
            title="No bringing up or commenting on any triggering comment")
        await ctx.channel.send(embed=embed)
    elif rule == 8:
        embed = discord.Embed(
            title="No recording in public video and voice channels")
        await ctx.channel.send(embed=embed)
    elif rule == 9:
        embed = discord.Embed(title="No DDoSing or DDoxing")
        await ctx.channel.send(embed=embed)
    elif rule == 10:
        embed = discord.Embed(title="Absolutely no bullying and/or harrasment")
        await ctx.channel.send(embed=embed)
    elif rule == 11:
        embed = discord.Embed(
            title="Abosolutely no death threats, they will not be tolerated")
        await ctx.channel.send(embed=embed)
    elif rule == 11:
        embed = discord.Embed(
            title="Copypasta is not allowed, please refrain from doing it")
        await ctx.channel.send(embed=embed)
    elif rule == 12:
        embed = discord.Embed(title="Don't spam ping others")
        await ctx.channel.send(embed=embed)
    elif rule == 13:
        embed = discord.Embed(title="Advertising is not allowed, contact the staff for permission")
        await ctx.channel.send(embed=embed) 
    else:
        await ctx.channel.send("Invalid rule option given")


@bot.command(name="uno", help="Command for playing uno")
async def uno(ctx, players):
    ctx.channel.send(
        "This command is still in development! it will be ready soon")


@bot.command(name="purge", help="Command for purging the last hundred messages in a channel")
@commands.has_any_role("Admin", "Moderator")
async def purge(ctx, amount: int = None):
    if amount == None:
        await ctx.channel.send("Please enter an amount")
    await ctx.channel.purge(limit=amount)


@bot.command(name="topic")
async def topic(ctx):
    topic = rd.choice(topics)
    await ctx.channel.send(topic)


@bot.command(name="wiki-search")
async def wiki_search(ctx, word):
    try:
        result = wikipedia.summary(word)
        await ctx.channel.send("Here is the wikipedia summary for your word: " + result)
    except:
        await ctx.channel.send("Sorry, I couldn't find a definition for your word")


@bot.command(name="get-headlines")
async def get_everthing(ctx, keyword, limit=10):
    top_headlines = newsapi.get_top_headlines(
        q=keyword,
        language="en",
    )
    counter = 1
    articleList = []
    descList = []
    for article in top_headlines['articles']:
        if counter == limit:
            break
        articleList.append(article['title'])
        descList.append(article['description'])
        counter += 1
    await ctx.channel.send(f"Found {len(articleList)} articles")
    for article in articleList:
        await ctx.channel.send("`" + article + "\n" + '`')


@bot.command(name="source")
async def source(ctx):
    embed = discord.Embed(
        title="https://github.com/AbooMinister25/InfiniteSpammersBot/blob/master/main.py")
    await ctx.channel.send(embed=embed)


@bot.command(name="request-topic")
async def request_topic(ctx, topic):
    requestedTopics.append(topic)
    await ctx.channel.send("Topic requested")


@bot.command(name="approve-topic")
@commands.has_any_role("Admin", "Moderator")
async def approve_topic(ctx, topic):
    if topic in requestedTopics:
        topics.append(topic)
        with open("data.json", 'r') as f:
            write_json(data)
        await ctx.channel.send("Topic approved")
    else:
        await ctx.channel.send("Sorry, the requested topic could not be found")


@bot.command(name="clear-topics")
@commands.has_any_role("Admin", "Moderator")
async def clear_topics(ctx):
    requestedTopics.clear()
    await ctx.channel.send("Requested topics cleared")


@bot.command(name="set-slowmode")
@commands.has_any_role("Admin", "Moderator")
async def set_slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.channel.send(f"Slowmode for the current channel has been set to {seconds} seconds")


@bot.command(name="sm")
@commands.has_any_role("Admin", "Moderator")
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.channel.send(f"Slowmode for the current channel has been set to {seconds} seconds")


@bot.command(name="get-role")
async def get_role(ctx, role):
    available_roles = ["<18", ">18", "He/Him", "She/Her", "They/Them", "North America",
                       "South America", "Europe", "Asia", "Australia", "Crewmates", "Game Night", "he/him", "she/her", "they/them", "north america",
                       "south america", "europe", "asia", "australia", "crewmates", "game night"]
    if role in available_roles:
        user = ctx.message.author
        role = get(user.guild.roles, name=role)
        await ctx.message.author.add_roles(role)
        await ctx.channel.send(f"Role {role} successfully added")
    else:
        await ctx.channel.send(f"Role {role} not found")


@bot.command(name="gr")
async def get_role(ctx, role):
    available_roles = ["<18", ">18", "He/Him", "She/Her", "They/Them", "North America",
                       "South America", "Europe", "Asia", "Australia", "Crewmates", "Game Night", "he/him", "she/her", "they/them", "north america",
                       "south america", "europe", "asia", "australia", "crewmates", "game night"]
    if role in available_roles:
        user = ctx.message.author
        role = get(user.guild.roles, name=role)
        await ctx.message.author.add_roles(role)
        await ctx.channel.send(f"Role {role} successfully added")
    else:
        await ctx.channel.send(f"Role {role} not found")


@bot.command(name="random-case")
async def random_case(ctx, string):
    rcaps_string = ''.join(rd.choice((str.upper, str.lower))(c)
                           for c in string)
    await ctx.channel.send(rcaps_string)


@bot.command(name="rc")
async def random_case(ctx, string):
    rcaps_string = ''.join(rd.choice((str.upper, str.lower))(c)
                           for c in string)
    await ctx.channel.send(rcaps_string)


@bot.command(name="general-name")
async def general_name(ctx, name):
    channel = bot.get_channel(id=791102724027580486)
    new_name = "general-" + name
    await channel.edit(name=new_name)
    await ctx.channel.send(f"General Name succesfully changed to {new_name}")


@bot.command(name="gn")
async def general_name(ctx, name):
    channel = bot.get_channel(id=791102724027580486)
    new_name = "general-" + name
    await channel.edit(name=new_name)
    await ctx.channel.send(f"General Name succesfully changed to {new_name}")


@bot.command(name="server-stats", aliases=["ss"])
async def server_stats(ctx, stats_type="All"):
    guild = ctx.guild
    channels_info = {
        "total categories": len(guild.categories),
        "total channels": len(guild.channels),
        "total text channels": len(guild.text_channels),
        "total voice channels": len(guild.voice_channels)
    }
    members_info = {
        "total users": guild.member_count,
        "total online members": sum(member.status == discord.Status.online and not member.bot for member in ctx.guild.members),
        "total offline members": sum(member.status == discord.Status.offline and not member.bot for member in ctx.guild.members),
        "total humans": sum(not member.bot for member in ctx.guild.members),
        "total bots": sum(member.bot for member in ctx.guild.members)
    }
    roles_info = {
        "total roles": len(guild.roles)
    }
    channels_message = f"""
    
    **Total Categories**:      {channels_info['total categories']}
    **Total Channels**:        {channels_info['total channels']}
    **Total Text Channels**:   {channels_info['total text channels']}
    **Total Voice Channels**:  {channels_info['total voice channels']}
"""
    members_message = f"""
    
    **Total Members**:         {members_info["total users"]}
    **All Online Members**:    {members_info["total online members"]}
    **All Offline Members**:   {members_info["total offline members"]}
    **All Human Users**:       {members_info["total humans"]}
    **All Bots**:              {members_info["total bots"]}
"""
    misc_message = f"""
    
    **All Roles**:             {roles_info['total roles']}
"""
    if stats_type == "All":
        embed = discord.Embed(title="Server Stats (All)",
                              color=discord.Colour.blue())
        embed.add_field(name="Channels Info",
                        value=channels_message, inline=False)
        embed.add_field(name="Members Info",
                        value=members_message, inline=False)
        embed.add_field(name="Miscellaneous", value=misc_message, inline=False)

    elif stats_type.lower() == "channels":
        embed = discord.Embed(
            title="Server Stats (Channels)", color=discord.Colour.blue())
        embed.add_field(name="Channels Info",
                        value=channels_message, inline=False)
    elif stats_type.lower() == "members":
        embed = discord.Embed(
            title="Server Stats (Members)", color=discord.Colour.blue())
        embed.add_field(name="Members Info",
                        value=members_message, inline=False)
    elif stats_type.lower() == "miscellaneous":
        embed = discord.Embed(
            title="Server Stats (Miscellaneous)", color=discord.Colour.blue())
        embed.add_field(name="Miscellaneous", value=misc_message, inline=False)
    else:
        await ctx.channel.send(f"Incorrect option {stats_type} given")

    await ctx.channel.send(embed=embed)


@bot.command(name="warn")
async def warn(ctx, member: discord.Member, *message):
    message = f"{ctx.message.author} warned {member}. {' '.join(message)}"
    await ctx.channel.send(message)


@bot.command(name="total-messages", aliases=["tm"])
async def total_messages(ctx, channel: discord.TextChannel=None):
    channel = channel or ctx.channel
    count = 0
    async for _ in channel.history(limit=None):
        count += 1
    embed = discord.Embed(title="Total Messages", description=f"Total messages sent in {channel.mention}: {count}", color=discord.Colour.purple())
    await ctx.channel.send(embed=embed)


@bot.command(name="embed", aliases=["e"])
async def embed(ctx, title, message, color: discord.Colour):
    embed = discord.Embed(title=title, description=message, color=color)
    await ctx.channel.send(embed=embed)


@bot.command(name="store", aliases=["st", "store-data", "s", "take-note", "note", "tn"])
async def store(ctx, title, data):
    with open('storage.json', 'r') as f:
        stored_data = json.load(f)
        stored_data[title] = data
    with open('storage.json', 'w') as f:
        json.dump(stored_data, f)
    embed = discord.Embed(title="Data stored succesfully", description="You can call this data using the !call or !retrieve commands", color=discord.Colour.green())
    await ctx.channel.send(embed=embed)


@bot.command(name="call", aliases=["retrieve"])
async def call(ctx, keyword: str):
    with open('storage.json', 'r') as f:
        data = json.load(f)
    try:
        data = data[keyword]
        embed = discord.Embed(title="Data Retrieved Succesfully", description=f"Data: {data}", color=discord.Colour.green())
    except:
        embed = discord.Embed(title="Data Retrieval Failed", description=f"Invalid keyword {keyword} given", color=discord.Colour.red())
    await ctx.channel.send(embed=embed)


@bot.command(name="hash")
async def hash_string(ctx, string):
    await ctx.channel.send(hash(string))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.channel.send("You are not authorized to use this command")
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send("Please enter the correct number of arguments for this command, do !help(command-name) for further help with this command")
    elif isinstance(error, commands.errors.MemberNotFound):
        await ctx.channel.send(f"Invalid member given, {error}")
    else:
        raise error


@bot.event
async def on_member_join(member: discord.Member):
    join_messages = [f"{member} has joined!", f"Welcome to our server, {member}", f"Hey {member}, glad to have you!",
                     f"Hey {member}, how long did it take you to get here?", f"It was getting quiet, glad you showed up {member}"
                     f"Hey {member}, feeling good about this server yet?"]
    channel = bot.get_channel(791453623379951638)
    message = rd.choice(join_messages)
    await channel.send(message)


@bot.event
async def on_ready():
    changeGeneralName.start()
    clear_storage.start()


@tasks.loop(hours=24)
async def changeGeneralName():
    channel = bot.get_channel(id=791102724027580486)
    x = rd.randint(1, 2)
    if x == 1:
        newName = "general-" + rd.choice(generalNames)
    else:
        newName = "general-" + rd.choice(customGeneralNames)
    await channel.edit(name=newName)


@tasks.loop(hours=48)
async def clear_storage():
    with open('storage.json', 'w') as f:
        x = {}
        json.dump(x, f)


@bot.command(name="help")
async def help(ctx, command="1"):
    if command == "ban":
        await ctx.channel.send("`ban  Moderator command for banning a user. Usage: !ban <user> <ban_message (optional)>`")
    elif command == "mute":
        await ctx.channel.send("`mute  Moderator command for muting a user. Usage: !mute <user>`")
    elif command == "unmute":
        await ctx.channel.send("`unmute  Moderator command for umuting a user. Usage: !mute <user>`")
    elif command == "silence":
        await ctx.channel.send("`silence  Moderator command for silencing the current channel, stops all users from sending messages. Usage:  !silence`")
    elif command == "unsilence":
        await ctx.channel.send("`unsilence  Moderator command for unsilencing the current channel. Usage: !unsilence`")
    elif command == "purge":
        await ctx.channel("`purge  Command for deleting a given amount of messages from the current channel. Usage: !purge <amount>`")
    elif command == "rule":
        await ctx.channel.send("`rule  Command for displaying a rule based on the given rule number. Usage: !rule <rule_number>`")
    elif command == 'def':
        await ctx.channel.send("`def  Command that returns the definition for a given word. Usage: !def <term>`")
    elif command == "poll":
        await ctx.channel.send("`poll  Command for creating a poll. Takes a topic and two reactions as arguments. Usage: !poll <pollname> <reaction1> <reaction2>`")
    elif command == "pronoun":
        await ctx.channel.send("`pronoun  Command for setting your pronoun. Usage: !pronoun <pronoun (he/him,she/her,they/them)>`")
    elif command == "create-channel":
        await ctx.channel.send("`create-channel  Command for creating a channel. Usage: !create-channel <chanel_name>`")
    elif command == "rename-channel":
        await ctx.channel.send("`rename-channel  Command for renaming a channel. Usage: !rename-channel <channel-name>`")
    elif command == "wiki-search":
        await ctx.channel.send("`wiki-search  Command that searches wikipedia for a given term and returns a definition. Usage: !wiki-search <word>`")
    elif command == "1":
        help_message1 = """
        ```
Page 1
Moderation

ban         Moderator command for for banning a user. Usage: !ban <user> <message>

mute        Moderator command for muting a user. Usage: !mute <user>

unmute      Moderator command for unmuting a given user. Usage: !unmute <user>

silence     Moderator command for silencing the current channel, stopping all messages from being sent.
            Usage: !silenced
            
unsilence   Moderator command for unsilencing the current channel. Usage: !unsilenced

set-slowmode Moderator command for setting a slowmode in the current channel. Usage: !set-slowmode <seconds>

warn        Moderator command for warning a given user. Usage: !warn <user> <message>
------------------------------------------------
Utilites

purge       Command for purging the current channel of a given amount of messages.
            Usage: !purge <amount>
            
rule        Command for displaying a given rule. Usage: !rule <rule_number>       

def         Command that returns a definition for the given word.
            Usage: !def <term>

wiki-search  Command for searching and getting a definition for a word from wikipedia.
            Usage: !wiki-search <word>
            
poll        Creates a poll. Usage: !poll <pollname> <reaction1> <reaction2>

pronoun     Command for setting your pronoun. Usage: !pronoun <pronoun>

create-channel  Command for creating a channel. Usage: !create-channel <channel-name>

rename-channel  Command for renaming a channel. Usage: !rename-channel <channel-name>

get-role        Command for users to claim a role. Usage: !get-role <role>
        ```
        """
        await ctx.channel.send(help_message1)
    elif command == "help":
        await ctx.channel.send("`help  Shows the help message. Takes an optinal command or page number for an argument. Usage: !help <command_name/page_number>`")
    elif command == "github":
        await ctx.channel.send("`github  Displays the link to the github page for this bot. Usage: !github`")
    elif command == "site":
        await ctx.channel.send("`site  Displays the link to our site. Usage: !site`")
    elif command == "request-general-name":
        await ctx.channel.send("`request-general-name  Command for requesting a name for the general channel. Usage: !request-general-name <name>`")
    elif command == "approve-request-general-name":
        await ctx.channel.send("`approve-requested-general-name  Command for approving a requested general name. Usage: !approve-requested-general-name <name>`")
    elif command == "display-requested-general-names":
        await ctx.channel.send("`display-requested-general-names  Command for displaying all the requested general names. Usage: !display-requested-general-names`")
    elif command == "clear-requested-general-names":
        await ctx.channel.send("`clear-reqested-general-names  Command for clearing all the requested general names. Usage: !clear-requested-general-names`")
    elif command == "clear-selected-general-name":
        await ctx.channel.send("`clear-selected-general-name  Command for clearing a given requested general name. Usage: !clear-selected-general-name <name>`")
    elif command == "topic":
        await ctx.channel.send("`topic  Displays a topic in the current channel. Usage: !topic`")
    elif command == "uno":
        await ctx.channel.send("`(coming soon) uno  Command for starting a game of uno. Usage: !uno`")
    elif command == "get-headlines":
        await ctx.channel.send("`get-headlines  Command for retrieving the latest headlines. Usage: !get-headlines <term> <(optional) limit>`")
    elif command == "source":
        await ctx.channel.send("`source  Command for displaying the link to the github page for this bot. Usage: !source`")
    elif command == "random-case":
        await ctx.channel.send("`random-case  Command for randomly capitalizing a given string. Usage: !random-case <string>`")
    elif command == "set-slowmode":
        await ctx.channel.send("`set-slowmode  Command for setting the slowmode of a current channel. Usage: !set-slowmode <seconds>`")
    elif command == "get-role":
        await ctx.channel.send("`get-role  Command for users to claim a certain role. Usage: !get-role <role>")
    elif command == "2":
        help_message2 = """
        ```
Page 2
Resources     
help        Displays this message, optional command name argument. Usage: !help <command_name>

site        Displays the link for our site. Usage: !site

github      Displays the link to the github page for this bot. Usage: !github

source      Displays the link to the github page for this bot. Usage: !source

--------------------------------------------------

Miscellaneous

request-general-name  Command for requesting a name for the general channel.
                        Usage: !request-general-name <name>
                        
approve-requested-general-name  Command for approving a requested general name.
                                Usage: !approve-requested-general-name <name>
                                
display-requested-general-names  Command for displaying all the requested general names.
                                    Usage: !display-requested-general-names
                                    
clear-requested-general-names   Command for clearing all the requested general names. 
                                Usage: !clear-requested-general-names
                                
clear-selected-general-name     Command for clearing a given requested general name.
                                Usage: !clear-selected-general-name <name>

topic           Displays a topic in the current channel. Usage: !topic

uno             (Coming Soon) Command for playing uno. Usage: !uno 
        ```
        """
        await ctx.channel.send(help_message2)
    elif command == "3":
        help_message3 = """
Page 3
Miscellaneous

get-headlines  Command for retrieving the latest headlines. Usage: !get-headlines <topic> <(optional)limit>

random-case: Command for randomly capitalizing letters in a given string. Usage: !random-case <string>

server-stats    Command for displaying a few of the servers statistics. Usage: !server-stats <Section (Default=All)>

total-messages  Command for displaying the total messages in a given channel, or the users current channel. Usage: !total-messages <channel-name>

embed           Command for creating embeds. Usage: !embed <title> <description> <color>

store           Command for storing data in a JSON file, all data deletes after 48 hours. Usage: !store <keyword> <data>

call            Command for retrieving stored data. Usage: !call <keyword>

        """
        await ctx.channel.send(help_message3)

bot.run(token)
