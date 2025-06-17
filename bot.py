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
    "2022-23": "data/2022-23.json",
    "2023-24": "data/2023-24.json",
    "2024-25": "data/2024-25.json",
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

    selected = random.sample(lineups, 5)
    message = ""
    for lineup in selected:
        team = lineup["team"]
        opponent = lineup["opponent"]
        date = lineup["date"]
        home = "Home" if lineup["is_home"] else "Away"
        starters = ", ".join(lineup["starters"])
        message += (
            f"**{team} vs {opponent}** ({home}) - {date}\nStarters: {starters}\n\n"
        )

    await ctx.send(message)


# Run bot
bot.run(TOKEN)
