import discord
from discord.ext import commands, tasks
import random
import json

with open("data.json", "r") as f:
    data = json.load(f)


generalNames = data["general-names"]
customGeneralNames = data["custom-general-names"]
topics = data["topics"]
requestedGeneralNames = []
requestedTopics = []

def get_join_message(member):
    join_messages = (f"Welcome to our server, {member}, have fun!", f"It was getting quiet, glad you showed up {member}!", f"Hey, {member}, why'd it take you so long to get here?",
                     f"Glad you could make it, {member}", f"Hey {member}, glad to have you!")
    message = random.choice(join_messages)
    return message

class ServerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_general_name.start()
        self.clear_storage.start()
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(id=791453623379951638)
        message = get_join_message(member)
        await channel.send(message)

    @tasks.loop(hours=24)
    async def change_general_name(self):
        channel = self.bot.get_channel(id=791102724027580486)
        x = random.randint(1, 2)
        if x == 1:
            newName = "general-" + random.choice(generalNames)
        else:
            newName = "general-" + random.choice(customGeneralNames)
        await channel.edit(name=newName)

    @tasks.loop(hours=48)
    async def clear_storage(self):
        with open('storage.json', 'w') as f:
            x = {}
            json.dump(x, f)


def setup(bot):
    bot.add_cog(ServerCog(bot))