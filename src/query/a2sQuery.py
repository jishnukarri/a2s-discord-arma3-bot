import a2s
import src.query.arma3query_e as arma3query_e
import datetime
from humanize import precisedelta
import asyncio
import logging


class Arma3Query:
    def __init__(self, serverTuple: tuple[str, int]) -> None:
        self.tuple: tuple[str, int] = serverTuple
        self.info: dict = {
            "name": "",
            "players": 0,
            "max_player": 0,
            "password_protected": False,
            "map_name": "",
        }
        self.rules: dict = {}
        self.players: dict[str, list] = {
            "heading": ["Player Name", "Kills", "Played Time"],
            "players": [],
        }
        self.isReady = False
        self.infoError = False
        logging.info(f"Server Object: {self.tuple} Init Success")
        self.start()

    async def getInformation(self):
        try:
            info = a2s.info(address=self.tuple)  # type: ignore
            self.info = {
                "name": str(info.server_name),
                "players": int(info.player_count),
                "max_player": int(info.max_players),
                "password_protected": info.password_protected,
                "map_name": info.map_name,
            }
            logging.info(f"Server Info: {self.tuple} Success")
            return self.info
        except Exception as e:
            logging.error(f"Server Info: {self.tuple} Failed", exc_info=True)
            self.infoError = True

    async def getRules(self):
        try:
            self.rules = arma3query_e.arma3rules(self.tuple).__dict__  # type: ignore
            logging.info(f"Server Rules: {self.tuple} Success")
            return self.rules
        except Exception as e:
            logging.error(f"Server Rules: {self.tuple} Failed", exc_info=True)
            self.infoError = True

    async def getPlayers(self):
        try:
            players = a2s.players(address=self.tuple)  # type: ignore
            playerObj = []
            for player in players:
                player.duration = precisedelta(
                    datetime.timedelta(seconds=player.duration)
                )
                playerObj.append([player.name, player.score, player.duration])
            self.players["players"] = playerObj
            logging.info(f"Server Players: {self.tuple} Success")
            return self.players
        except Exception as e:
            logging.error(f"Server Players: {self.tuple} Failed", exc_info=True)
            self.infoError = True

    async def autoUpdateLoop(self, interval=10):
        self.running = True
        while self.running:
            try:
                await self.getInformation()
                # await self.getRules() currently rules are not purposed for anything
                await self.getPlayers()
                if self.infoError != True:
                    self.isReady = True
                await asyncio.sleep(interval)
                logging.info(f"AutoUpdate Server Information: {self.tuple} Success")
            except Exception as e:
                logging.error(
                    f"AutoUpdate Server Information: {self.tuple} Failed", exc_info=True
                )

    # Propertry's

    @property
    def reqInfo(self):
        return self.info

    @property
    def reqRules(self):
        return self.rules

    @property
    def reqPlayers(self):
        return self.players

    def start(self):
        if self.task is None or self.task.done():
            self.task = asyncio.create_task(self.autoUpdateLoop())

    def stop(self):
        self.task.cancel()
