import discord
import logging
from src.query.a2sQuery import Arma3Query
from src.config import *
from tabulate import tabulate
from datetime import datetime
import humanize
import time
import asyncio


# self.mainObject = {
#     "serverQueryObject": [], #["Name of the server from config",OBJECT]
#     "serverInformation": [
#         {
#             "serverName": "a2sServerName",
#             "serverPlayerCount": 0,
#             "serverMaxPlayer":0,
#             "serverPlayerTable": None,
#             "passworded": False,
#               "map_name": ""
#         }
#     ] #
# }
# Conceptual: Pointing directly to the live data structure in memory - from gemini
# self.mainObject["serverInformation"][0]["serverPlayerTable"] = self.mainObject["serverQueryObject"][1].live_player_data


class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainObject = {"serverQueryObject": {}, "serverInformation": {}}

    async def on_ready(self):
        logging.info(f"Discord bot ready as {self.user}")
        channel = self.get_channel(CHANNEL_ID)
        if not hasattr(self, "initialized"):  # checks init
            if isinstance(channel, discord.TextChannel):
                self.channel = channel


                for server in DATABASE_CONFIG.get("servers"):
                    # This attaches the vars to live data structure in memory
                    self.mainObject["serverQueryObject"][str(server[0])] = Arma3Query(
                        tuple(server[1])
                    )
                    self.mainObject["serverQueryObject"][str(server[0])].start()
                    while (
                        self.mainObject["serverQueryObject"][str(server[0])].isReady
                        == False
                    ):
                        await asyncio.sleep(0.5)
                    await self.initStatusEmbed()

                    self.init = True

    async def updateServerInfo(self,interval=8):
        running = True

        while running:
            for server in DATABASE_CONFIG.get("servers"):
                sStuct = {
                    "serverPlayerCount": self.mainObject["serverQueryObject"][
                        server[0]
                    ].reqInfo["players"],
                    "serverMaxPlayer": self.mainObject["serverQueryObject"][
                        server[0]
                    ].reqInfo["max_player"],
                    "serverPlayerTable": tabulate(
                        self.mainObject["serverQueryObject"][server[0]].reqPlayers[
                            "players"
                        ],
                        headers=["Name", "Kills", "Time"],
                        tablefmt="double_outline",
                        stralign="left",  # text alignment
                        numalign="left",  # number alignment
                    ),
                    "passworded": self.mainObject["serverQueryObject"][
                        server[0]
                    ].reqInfo["password_protected"],
                    "map_name": self.mainObject["serverQueryObject"][server[0]].reqInfo[
                        "map_name"
                    ],
                }
                title = self.mainObject["serverQueryObject"][server[0]].reqInfo["name"]
                self.mainObject["serverInformation"][title] = sStuct

                await asyncio.sleep(interval)
    async def updateStatusMessage(self, interval=10):
        running = True
        while running:
            print("I got called update")
            sent: bool = False
            while sent == False:
                if self.channel:
                    """
                    emoji for locked/passsworded : 🔒
                    

                    command to generate table
                    """
                    if len(self.mainObject["serverInformation"]) <= 1:
                        name = DATABASE_CONFIG["community_info"]["name"] or ""
                        for server in self.mainObject["serverInformation"]:
                            server = self.mainObject["serverInformation"][server]
                            playerCount = f"{str(server['serverPlayerCount'])} / {str(server['serverMaxPlayer'])}"
                            playerMap = server["map_name"]
                            playersTable = server["serverPlayerTable"]

                            message = discord.Embed(
                                color=discord.Color.from_str("#a51e1e"),
                                title=f"{name}'s Server - {playerCount} - {playerMap}",
                                description=f"```{playersTable}```",
                                timestamp=datetime.now(),
                            )

                        # Todo: once A2S built
                    messageID = DATABASE_CONFIG["messageId"]["status"]
                    if messageID == 0:
                        messageSent = await self.channel.send(embed=message)  # type: ignore
                        addToDatabase(["messageId", "status"], messageSent.id)
                        sent = True
                    try:
                        messageId = await self.channel.fetch_message(messageID)
                        await messageId.edit(embed=message)  # type: ignore
                        sent = True
                    except:
                        messageSent = await self.channel.send(embed=message)  # type: ignore
                        addToDatabase(["messageId", "status"], messageSent.id)
                        sent = True
                await asyncio.sleep(interval)

    async def initStatusEmbed(self):
        self.ServerTask = asyncio.create_task(self.updateServerInfo())
        # code which sends the message
        sent: bool = False
        while sent == False:
            if self.channel:
                """
                emoji for locked/passsworded : 🔒
                

                command to generate table
                """
                if len(self.mainObject["serverInformation"]) <= 1:
                    name = DATABASE_CONFIG["community_info"]["name"] or ""
                    for server in self.mainObject["serverInformation"]:
                        server = self.mainObject["serverInformation"][server]
                        playerCount = f"{str(server['serverPlayerCount'])} / {str(server['serverMaxPlayer'])}"
                        playerMap = server["map_name"]
                        playersTable = server["serverPlayerTable"]

                        message = discord.Embed(
                            color=discord.Color.from_str("#a51e1e"),
                            title=f"{name}'s Server - {playerCount} - {playerMap}",
                            description=f"```{playersTable}```",
                            timestamp=datetime.now(),
                        )

                    # Todo: once A2S built
                messageID = DATABASE_CONFIG["messageId"]["status"]
                if messageID == 0:
                    messageSent = await self.channel.send(embed=message)  # type: ignore
                    addToDatabase(["messageId", "status"], messageSent.id)
                    sent = True
                try:
                    messageId = await self.channel.fetch_message(messageID)
                    await messageId.edit(embed=message)  # type: ignore
                    sent = True
                except:
                    messageSent = await self.channel.send(embed=message)  # type: ignore
                    addToDatabase(["messageId", "status"], messageSent.id)
                    sent = True
        self.messageTask = asyncio.create_task(self.updateStatusMessage())

