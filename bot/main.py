import discord
from discord.ext import commands

def get_token():
    with open("token.txt") as f:
        token = f.read()
    return token

bot = commands.Bot(command_prefix="!", help_command=None)

extensions = [
    "moderation.moderation",
    "moderation.silence",
    "moderation.slowmode",
    "utilities.utils",
    "utilities.serverconfig",
    "utilities.poll",
    "utilities.resources"
]

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

bot.run("NzQ1Mzk5MDQzMDY0MjAxMjU3.XzxM9A.tSf5U4RuvupmJNb1HjdzAV87Jso")