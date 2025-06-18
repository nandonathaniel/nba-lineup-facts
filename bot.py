import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
import random
import os

load_dotenv()  # Loads variables from .env
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

SEASON_FILES = {
    "2022-23": "data/new-2022-23.json",
    "2023-24": "data/new-2023-24.json",
    "2024-25": "data/new-2024-25.json",
}


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command(name="randomlineup")
async def randomlineup(ctx, season: str):
    print(f"Command received: {season}")
    if season not in SEASON_FILES:
        await ctx.send(f"Invalid season! Choose from: {', '.join(SEASON_FILES.keys())}")
        return

    file_path = SEASON_FILES[season]
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lineups = json.load(f)
    except Exception as e:
        await ctx.send(f"Failed to load data for {season}: {e}")
        return

    if len(lineups) < 5:
        await ctx.send(f"Not enough data in {season} to pick 5 lineups.")
        return

    selected = random.sample(lineups, 1)
    message = ""
    for lineup in selected:
        team = lineup["team"]
        opponent = lineup["opponent"]
        date = lineup["date"]
        if lineup["is_home"]:
            message += f"**{team}** vs. {opponent} on {date}\n"
        else:
            message += f"**{team}** @ {opponent} on {date}\n"
        position_order = {"G": 0, "F": 1, "C": 2}
        sorted_starters = sorted(
            lineup["starters"], key=lambda x: position_order.get(x[0], 3)
        )

        for starter in sorted_starters:
            position, player_name, player_id = starter
            message += f"{position}: {player_name}\n"

    await ctx.send(message)


# Run bot
bot.run(TOKEN)
