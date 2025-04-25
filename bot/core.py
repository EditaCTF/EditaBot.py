import discord
from discord.ext import commands

def create_bot(intents, command_prefix="$"):
    return commands.Bot(command_prefix=command_prefix, intents=intents)
