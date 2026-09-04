from src.query.a2sQuery import Arma3Query
from src.config import DATABASE,CONFIG
import discord 
from discord.ext import commands,tasks
import logging
import asyncio
import tabulate

servers = []
loaded = False

class Server:
    def __init__(self, ip, port,name) -> None:
        self.ip = ip
        self.port = port
        self.name = name
        self.createObject()

    def createObject(self):
        self.object = Arma3Query(
            ip=self.ip,
            port=self.port,
            jsonName=self.name
        )

    @property
    def info(self):
        return self.object.info
    @property
    def players(self):
        return self.object.players
    @property
    def isActive(self):
        if self.object.failedRetries <= 10:
            return True
        else:
            return False
    @property
    def getTable(self):
        if self.object.lastUpdated == 0:
            table = tabulate.tabulate([["Loading","Data","..."]],["Name","Score","Time Played"])
        else:
            _players =  []
            for i in self.players[:10]:
                _players.append(list(i))
            table = tabulate.tabulate(_players,["Name","Score","Time Played"])
        return table


class Bot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(intents=intents) 
        super().run(token=CONFIG.CLIENT_TOKEN) 
    async def setup_hook(self):
        if loaded != True:
            pass
        for server in DATABASE.serversDATA:
            _ser = Server(name=server.name,ip=server.ip,port=server.port)
            servers.append(_ser)

    async def on_ready(self):
        loaded = True
        logging.info(f"Bot is loaded as {self.user.name}({self.user.id})") # type: ignore
        self.serverStatusUpdater.start()

    def generateServerStatusEmbed(self):
        embed = discord.embeds.Embed()
        embed.title = f"{DATABASE.guildDATA.communityName}'s Server Status"
        embed.color = discord.Color.default()
        for server in servers:
            if server.isActive == True:
                embed.add_field(
                    name=server.info.name or server.name,
                    value=f"```\n {server.getTable} \n```",
                    inline=True
                )

        return embed
    
    @tasks.loop(seconds=10)
    async def serverStatusUpdater(self):
        channel = self.get_channel(CONFIG.CHANNEL_ID)
        if isinstance(channel,discord.TextChannel):
            id = DATABASE.messageDATA.statusMessageID
            if id == 0:
                _emebed = self.generateServerStatusEmbed()
                message = await channel.send(embed=_emebed)
                DATABASE.updateMessageID(message.id)
            else:            
                try:
                    message = await channel.fetch_message(id)
                    _emebed = self.generateServerStatusEmbed()
                    await message.edit(embed=_emebed)
                except Exception as e:
                    _emebed = self.generateServerStatusEmbed()
                    message = await channel.send(embed=_emebed)
                    DATABASE.updateMessageID(message.id)
    