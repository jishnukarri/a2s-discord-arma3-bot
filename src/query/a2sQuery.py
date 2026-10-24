import a2s
from a2s.exceptions import BrokenMessageError, BufferExhaustedError
lazy import src.query.arma3query_e as arma3query_e
from src.data_models import ArmaInfo,Player

from datetime import datetime
from humanize import naturaldelta
import asyncio
import logging


class Arma3Query:
    def __init__(self, ip: str, port: int, jsonName) -> None:
        self.ip: str = ip
        self.port: int = port
        self.serverTuple: tuple[str, int] = (self.ip, self.port)
        self.jsonName: str = jsonName  # only way to conntect json db to the object
        # values
        self.info = None
        self.players: list[Player] = []
        # inital values
        self.lastUpdated: float = 0
        self.running: bool = True
        self.failedRetries: int = 0  # no.of times server failed to respond
        self.delayedTimeout = 10  # stays 10 if server is active; changes to 60 after 200 failures in a row
        self.autoLoopTask = asyncio.create_task(self.loopServerUpdates())

    def _dataUpdated(self):
        self.lastUpdated = datetime.now().timestamp()

    async def loopServerUpdates(self):
        while self.running == True:
            oldUpdated = self.lastUpdated

            await asyncio.to_thread(self._getInfo)
            await asyncio.to_thread(self._getPlayers)


            if self.failedRetries >= 200:
                self.delayedTimeout = 60
            else:
                self.delayedTimeout = 10

            if oldUpdated < self.lastUpdated:
                logging.debug(f"Data has been auto-updated for {self.serverTuple}")

            await asyncio.sleep(self.delayedTimeout)

    """
    Methods which update the server infromation
    """

    def _getInfo(self):
        try:
            info = a2s.info(self.serverTuple)  # type: ignore
            self.info = ArmaInfo(
                name=info.server_name,
                players=info.player_count,
                maxPlayers=info.max_players,
                passwordProtected=info.password_protected,
                mapName=info.map_name,
            )
            logging.debug(f"Current information for {self.serverTuple} has been updated")
            self.failedRetries = 0  # reset the consecutive-failure counter
            self._dataUpdated()
            pass
        except(BufferExhaustedError,TimeoutError):
            self.failedRetries += 1
            logging.warning(f"{self.serverTuple} did not respond to info query ({self.failedRetries} in a row)")
        except BrokenMessageError:
            self.failedRetries += 1
            logging.warning(f"{self.serverTuple} sent a broken info reply ({self.failedRetries} in a row)")
        except Exception as e:
            self.failedRetries += 1
            logging.exception(f"{self.serverTuple} info query failed unexpectedly: {e}")

    def _getPlayers(self):
        try:
            players = a2s.players(self.serverTuple)  # type: ignore
            playerArray = []
            for player in players:
                _localplayer = Player(
                    player.name, player.score, naturaldelta(player.duration)
                )
                playerArray.append(_localplayer)
            self.players = playerArray
            logging.debug(f"Current player list for {self.serverTuple} has been updated")
            self.failedRetries = 0  # success: reset the consecutive-failure counter
            self._dataUpdated()
            pass
        except(BufferExhaustedError,TimeoutError):
            self.failedRetries += 1
            logging.warning(f"{self.serverTuple} did not respond to players query ({self.failedRetries} in a row)")
        except BrokenMessageError:
            self.failedRetries += 1
            logging.warning(f"{self.serverTuple} sent a broken players reply ({self.failedRetries} in a row)")
        except Exception as e:
            self.failedRetries += 1
            logging.exception(f"{self.serverTuple} players query failed unexpectedly: {e}")
