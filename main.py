import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

from bot.db import load_data, save_data
from bot.ai import configure_gemini
from bot.events import setup_events
from bot.commands.admin import setup_admin_commands
from bot.commands.team import setup_team_commands
from bot.commands.question import setup_question_commands
from bot.commands.leaderboard import setup_leaderboard_commands
from bot.commands.utility import setup_utility_commands

load_dotenv()
gemini_api = os.getenv("GEMINI_API_KEY")
discord_token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

db = load_data()
for key in ["user_details", "teams", "question"]:
    if key not in db:
        db[key] = {}
        save_data(db)

client = commands.Bot(command_prefix="$", intents=intents)

chat = configure_gemini(gemini_api)

setup_events(client, chat)
setup_admin_commands(client, db, save_data)
setup_team_commands(client, db, save_data)
setup_question_commands(client, db, save_data)
setup_leaderboard_commands(client, db)
setup_utility_commands(client)

if __name__ == "__main__":
    client.run(discord_token)
