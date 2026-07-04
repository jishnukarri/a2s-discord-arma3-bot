from src.config import CLIENT_TOKEN
from src.bot.main import *
import discord
import logging

# 1. Setup basic logging configuration for the terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

intents = discord.Intents.default()

bot = DiscordBot(intents=intents)
bot.run(CLIENT_TOKEN)
