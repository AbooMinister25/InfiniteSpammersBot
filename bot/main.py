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
    "utilities.resources",
    "server.server",
    "server.errors",
    "server.general"
]

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

bot.run(get_token())