import discord
from discord.ext import commands
from PyDictionary import PyDictionary
import wikipedia
from newsapi import NewsApiClient
import json
import random
from typing import Optional


dictionary = PyDictionary()
newsapi = NewsApiClient(api_key='7458c5de548342898784767cecc360a7')


with open("data.json", "r") as f:
    data = json.load(f)

topics = data["topics"]
requested_topics = []


rules = ["No mass mentions such as @everyone or @here", "No pinging the staff unless necesarry",
         "Absolutely no hate speech, homophobia, sexism, racism, or any degrading comments or topics", "No NSFW content, keey the server friendly for everyone",
         "No innappropriate language or racial slurs", "No unnecesarry spamming", "No bringing up or commenting on any triggering topics"
         "No recording in public video and voice channels unless streaming or have permission from the mods", "No DDoSing or DDoxing", "Abosolutely no bullying and/or harrasment, will result in a mute/ban."
         "Death threats will not be tolerated", "Copypasta is not allowed", "Don't spam ping others", "Advertising is not allowed"]


class UtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="`!purge [amount]`. Used for deleting a specified number of messages in the current channel.", help="`!purge [amount]`. Used for deleting a specified number of messages in the current channel. This will delete the number of messages specified one by one. Moderator only command.")
    @commands.has_permissions(ban_members=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @commands.command(name="def", brief="`!def [word]`. Used for getting the dictionary definition of a word.", help="`!def [word]`. Used for getting the dictionary definition of a given word. Can be used to retrieve information and definitions of a word.")
    async def define(self, ctx, word: str):
        try:
            result = dictionary.meaning(word)
            embed = discord.Embed(
                title=f"{word}", description=f"{result}",  color=discord.Colour.green())
            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send(f":x: No definition found for word {word}",  color=discord.Colour.red())

    @commands.command(brief="`!rule [num]`. Used for displaying a specified rule.", help="`!rule [num]`. Used for displaying a specified rule. Can be used as a warning to a user that has violated a rule. Displays the rule in an embed in the current channel.")
    async def rule(self, ctx, rule):
        rule = int(rule)
        orig_rule = rule
        if rule == 1:
            rule_num = 0
        else:
            rule_num = rule
        try:
            rule = rules[rule_num]
            embed = discord.Embed(
                title=f"Rule {orig_rule}", description=rule, color=discord.Colour.blue())
        except:
            embed = discord.Embed(
                title=f":x: Invalid rule number {rule_num} given", color=discord.Colour.red())
        await ctx.channel.send(embed=embed)

    @commands.command(name="wiki-search", aliases=["ws"], brief="`!wiki-search [term]`. Used for getting a wikipedia summary of a given term.", help="`!wiki-search [term]`. Used for getting a wikipedia summary of a given term. Scours wikipedia and finds a relevant summary for the given term.")
    async def wiki_search(self, ctx, word):
        try:
            result = wikipedia.summary(word)
            embed = discord.Embed(
                title=f"Wikipedia Summary For Word: {word}", description=result, color=discord.Colour.green())
        except:
            embed = discord.Embed(
                title=f":x: Failed to find summary for given word {word}", color=discord.Colour.red())
        await ctx.channel.send(embed=embed)

    @commands.command(name="get-headlines", aliases=["gh"], brief="`!get-headlines [keyword] <limit>`. Used for getting the headlines on a given keyword.", help="`!get-headlines [keyword] <limit>`. Used for getting the headlines on a given keyword. Has a default result limit of 10. This limit can be changed as specified by the user.")
    async def get_headlines(self, ctx, keyword, limit: int = 10):
        top_headlines = newsapi.get_top_headlines(
            q=str(keyword),
            language="en",
        )
        counter = 1
        articles = {}
        articleList = []
        for article in top_headlines['articles']:
            if counter == limit:
                break
            articles[article["title"]] = article["description"]
            articleList.append(article['title'])
            counter += 1
        if len(articleList) != 0:
            embed = discord.Embed(
                title=f"Articles Found On {keyword}: {len(articleList)}", color=discord.Colour.orange())
            for article in articleList:
                embed.add_field(name=article, value=articles[article])
        else:
            embed = discord.Embed(
                title=f":x: Zero Articles Found On {keyword}")
        await ctx.send(embed=embed)

    @commands.command(name="server-stats", aliases=["ss", "s-s"], brief="`!server-stats <category>`. Used to display information on the server and can be filtered by category.", help="`!server-stats <category>`. Used to display information on the server and can be filtered by category. Has four categories, the default one of All, Members, Channels, and Roles.")
    async def server_stats(self, ctx, stats_type="All"):
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
            embed.add_field(name="Miscellaneous",
                            value=misc_message, inline=False)

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
            embed.add_field(name="Miscellaneous",
                            value=misc_message, inline=False)
        else:
            await ctx.channel.send(f"Incorrect option {stats_type} given")

        await ctx.channel.send(embed=embed)

    @commands.command(name="total-messages", aliases=["tm"], brief="`!total-messages <channel>`. Used for getting the total number of messages sent in a channel.", help="`!total-messages <channel>`. Used for getting the total number of messages sent in a channel. If a channel is not provided, the total messages of the current channel will be retrieved. This is the slowest command, and can take some time to execute, so be patient.")
    async def total_messages(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        count = 0
        async for _ in channel.history(limit=None):
            count += 1
        embed = discord.Embed(
            title="Total Messages", description=f"Total messages sent in {channel.mention}: {count}", color=discord.Colour.purple())
        await ctx.channel.send(embed=embed)

    @commands.command(name="embed", aliases=["e"], brief="`!embed [title] [description] [color]`. Used to create an embed with the provided arguments.", help="`!embed [title] [description] [color]`. Used to create an embed with the provided arguments. The title is the heading of the embed, the description is the content, and the color is the color of the embed.")
    async def embed(self, ctx, title, description, color: discord.Colour):
        embed = discord.Embed(
            title=title, description=description, color=color)
        await ctx.channel.send(embed=embed)

    @commands.command(name="store", aliases=["st", "store-data", "s", "take-note", "note", "tn"], brief="`!store [keyword] [data]`. Used for storing data that is classified by a given keyword.", help="`!store [keyword] [data]`. Used for storing data that is classified by a given keyword. This data can then be accessed by the `!call` command and is found by a passed keyword. All data expires after 48 hours.")
    async def store(ctx, title, data):
        with open('storage.json', 'r') as f:
            stored_data = json.load(f)
            stored_data[title] = data
        with open('storage.json', 'w') as f:
            json.dump(stored_data, f)
        embed = discord.Embed(title=":white_check_mark: Data stored succesfully",
                              description="You can call this data using the !call or !retrieve commands", color=discord.Colour.green())
        await ctx.channel.send(embed=embed)

    @commands.command(name="call", aliases=["retrieve"], brief="`!call [keyword]`. Used to retrieve data stored by the `!store` command..", help="`!call [keyword]`. Used to retrieve stored data with a given keyword specified in the `!store` command. All data expires after 48 hours.")
    async def call(ctx, keyword: str):
        with open('storage.json', 'r') as f:
            data = json.load(f)
        try:
            data = data[keyword]
            embed = discord.Embed(title=":white_check_mark: Data Retrieved Succesfully",
                                  description=f"Data: {data}", color=discord.Colour.green())
        except:
            embed = discord.Embed(title=":x: Data Retrieval Failed",
                                  description=f"Invalid keyword {keyword} given", color=discord.Colour.red())
        await ctx.channel.send(embed=embed)

    @commands.command(name="random-case", aliases=["rc"], brief="`!random-case [string]`. Used to randomly capitalize the letters in a given string.", help="`!random-case [string]`. Used to randomly capitalize the letters in a given string. The output will look something like `rAndOmIzEd stRinG`.")
    async def random_string(self, ctx, string):
        rcaps_string = ''.join(random.choice((str.upper, str.lower))(c)
                               for c in string)
        await ctx.channel.send(rcaps_string)

    @commands.command(brief="`!topic`. Used for displaying a converstaion topic.", help="`!topic`. Used for displaying a converstaion topic. New topics can be requested. Can be used to deter conversations or start new ones.")
    async def topic(self, ctx):
        topic = random.choice(topics)
        embed = discord.Embed(
            title="Topic", description=topic, color=discord.Colour.blue())
        embed.add_footer(text="Request new topics with `!request-topic`.")
        await ctx.channel.send(embed=embed)

    @commands.command(name="request-topic", brief="`!request-topic [topic]`. Used to request a new topic.", help="`!request-topic [topic]`. Used to request a new topic. Requested topics then have to be approved by a moderator.")
    async def request_topic(self, ctx, topic):
        requested_topics.append(topic)

    @commands.command(name="approve-topic", aliases=["at"], brief="`!approve-topic [topic]`. Used to approve a requested topic.", help="`!approve-topic [topic]`. Used to approve a requested topic. Will approve a requested topic that is specified by the user. Moderator only command.")
    @commands.has_permissions(ban_members=True)
    async def approve_topic(self, ctx, topic):
        if topic in requested_topics:
            data["topics"].append(topic)
            topics.append(topic)
            requested_topics.remove(topic)
            embed = discord.Embed(
                title=f":white_check_mark: Topic {topic} successfully approved.", color=discord.Colour.green())
        else:
            embed = discord.Embed(
                title=f":x: No topic {topic} found.", color=discord.Colour.red())

        await ctx.channel.send(embed=embed)

    @commands.command(name="clear-topics", aliases=["ct"], brief="`!clear-topics`. Used to clear all requested topics.", help="`!clear-topics`. Used to clear all requested topics. All of the requested topics will be cleared.")
    @commands.has_permissions(ban_members=True)
    async def clear_topics(self, ctx):
        requested_topics.clear()
        await ctx.channel.send(":white_check_mark: Succesfully cleared all requested topics")

    @commands.command(name="remove-topic", aliases=["clear-specified-topic", "remove-specified-topic", "clear-topic", "rt", "cst", "rst"], brief="`!remove-topic [topic]`. Removes the specified requested topic.", help="`!remove-topic [topic]`. Removes the specified requested topic. Can be used if a moderator thinks that a topic is not fit for the server. Moderator only command.")
    @commands.has_permissions(ban_members=True)
    async def remove_topic(self, ctx, topic):
        if topic in requested_topics:
            requested_topics.remove(topic)
            await ctx.channel.send(f":white_check_mark: Topic {topic} successfully removed.")
        else:
            await ctx.channel.send(f":x: Topic {topic} could not be found.")

    @commands.command(aliases=["ᓚᘏᗢ", "ᓚᘏᗢify"])
    async def catify(self, ctx, string: Optional[str] = None) -> None:
        if string is None:
            if len(ctx.author.name) > 28:
                await ctx.send("Your name exceeds character limits after catification. Please change your name!")
            else:
                await ctx.author.edit(nick=ctx.author.name + "ᓚᘏᗢ")
        else:
            string_list = string[6:len(string)].split()
            for index, name in enumerate(string_list):
                if "cat" in name:
                    string_list[index] = string_list[index].replace("cat", 'ᓚᘏᗢ')

            for i in range(random.randint(1, len(string_list)//3)):
                # insert cat at random index
                string_list.insert(random.randint(0, len(string_list)-1), "ᓚᘏᗢ")

            await ctx.channel.send(" ".join(string_list))


def setup(bot):
    bot.add_cog(UtilsCog(bot))
