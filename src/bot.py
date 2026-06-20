import logging
import discord
from discord.ext import tasks, commands
from src.config import CHANNEL_ID, GUILD_ID, TITLE, FOOTER, FOOTER_ICON, DATABASE_FILE
from src.serverRegistry import serverRegistry
from src.embed import Embeds
import src.serverQuery as serverQuery
import asyncio
import time
import src.database as database

logger = logging.getLogger(__name__)


class EmbedServerObject:
    def __init__(self, name, current_players, max_players, players_list, rules):
        self.name = name
        self.current_players = current_players
        self.max_players = max_players
        self.player_table = (
            ([[p.name, p.kills, p.time] for p in players_list] if players_list else []),
        )
        self.rules = rules
        self.last_updated = "Just Now"


class DiscordBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

        self.serverRegistry = serverRegistry()
        self.database = database.BotDatabase(DATABASE_FILE)

        self.query_engines = {}
        for gServer, data in self.serverRegistry.active_servers.items():
            server_host = str(data.get("address"))
            server_port = int(data.get("port") + 1)
            self.query_engines[gServer] = serverQuery.a2sQuery(
                (server_host, server_port), gServer
            )
        self.serverCache = {}

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")

    async def setup_hook(self):
        self.updateGithubServerData.start()
        self.updateServersInformation.start()
        await asyncio.sleep(3)  # was time.sleep() — blocked the event loop
        self.updateServerStatus.start()

    def syncLocalToRemoteData(self):
        current_registry = self.serverRegistry.active_servers

        # Add new servers from registry not yet in query_engines
        for gServer, data in current_registry.items():
            if gServer not in self.query_engines:
                server_host = str(data.get("address"))
                server_port = int(data.get("port") + 1)
                self.query_engines[gServer] = serverQuery.a2sQuery(
                    (server_host, server_port), gServer
                )

        # Remove servers no longer in registry — iterate a copy to allow deletion
        for gServer in list(self.query_engines.keys()):
            if gServer not in current_registry:
                del self.query_engines[gServer]
                self.serverCache.pop(gServer, None)

    @tasks.loop(minutes=10)
    async def updateGithubServerData(self):
        logger.info("Checking GitHub for registry updates...")
        self.serverRegistry.fetch_map_servers()
        self.syncLocalToRemoteData()

    @tasks.loop(seconds=10)
    async def updateServersInformation(self):
        localTickData = {}

        for gServer, data in self.serverRegistry.active_servers.items():
            a2s_object = self.query_engines.get(gServer)

            if a2s_object is None:
                logger.warning(f"No query engine for {gServer}, skipping.")
                continue

            info = a2s_object.getServerInfo()

            if not info:
                logger.error(f"{gServer} not responding to query - skipping.")
                continue

            server_settings = a2s_object.getServerRules()
            players = a2s_object.getServerPlayers()

            localTickData[gServer] = EmbedServerObject(
                name=gServer,
                current_players=info.player_count,
                max_players=info.max_players,
                players_list=players,
                rules=server_settings.__dict__ if server_settings else {},
            )

        self.serverCache = localTickData

    @tasks.loop(seconds=35)
    async def updateServerStatus(self):
        if not self.is_ready():
            return

        channel = self.get_channel(CHANNEL_ID)
        if not channel:
            try:
                channel = await self.fetch_channel(CHANNEL_ID)
            except Exception as e:
                logger.error(f"Could not fetch channel {CHANNEL_ID}: {e}")
                return

        # serverCache is keyed by server name — get all values as a list
        serverData = list(self.serverCache.values())
        if not serverData:
            logger.warning("serverCache is empty, skipping status update.")
            return

        self.discordEmbed = Embeds(TITLE, FOOTER, FOOTER_ICON)
        statusEmbed = self.discordEmbed.createServerStatus(servers=serverData)

        dbMessage = self.database.getMessageID()
        if dbMessage.get("status") != True:
            message = await channel.send(embed=statusEmbed)
            self.database.updateMessageID({"statusMsg": message.id})
            logger.info("Status message sent")
        else:
            try:
                    # Attempt to fetch and edit the existing message
                    message = await channel.fetch_message(dbMessage.get("statusMsg"))
                    await message.edit(embed=statusEmbed)
                    logger.info("Status message edited")
            except discord.NotFound:
                # Fallback: Create a new message if the old one was deleted
                logger.warning("Status message not found in channel. Creating a new one.")
                message = await channel.send(embed=statusEmbed)
                self.database.updateMessageID({"statusMsg": message.id})
                logger.info("New status message sent after original was not found")

    @updateServerStatus.before_loop
    async def before_serverStatus(self):
        await self.wait_until_ready()