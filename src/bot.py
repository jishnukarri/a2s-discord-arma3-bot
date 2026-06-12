import logging
import discord
from config import CLIENT_TOKEN

logger = logging.getLogger("discord")


class DiscordBot(discord.Client):
    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")


intents = discord.Intents.default()
intents.message_content = True  # enables it to see all messages *i think

client = DiscordBot(intents=intents)
client.run(CLIENT_TOKEN)
