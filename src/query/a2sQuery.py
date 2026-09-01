import a2s
from a2s.exceptions import BrokenMessageError, BufferExhaustedError
import src.query.arma3query_e as arma3query_e
from datetime import datetime
from humanize import precisedelta
import asyncio
import logging


class ArmaInfo:
    def __init__(
        self,
        name: str,
        players: int,
        maxPlayers: int,
        passwordProtected: bool,
        mapName: str,
    ) -> None:
        self.name = name
        self.players = players
        self.maxPlayers = maxPlayers
        self.passwordProtected = passwordProtected
        self.mapName = mapName

class Player:
    def __init__(self,name:str,score:int,time:int) -> None:
        self.name = name
        self.score = score 
        self.time = time


class Arma3Query:
    def __init__(self,ip:str,port:int,jsonName) -> None:
        self.ip:str = ip
        self.port:int = port
        self.serverTuple: tuple[str, int] = (self.ip,self.port)
        self.jsonName:str = jsonName # only way to conntect json db to the object
        # values
        self.info = None
        self.players:list[Player] = []
        #inital values
        self.lastUpdated: float = 0
        self.running:bool = True
        self.failedRetries:int = 0 #no.of times server failed to respond
        self.delayedTimeout = 10 #stays 10 if server is active; changes to 60 if the server failes to respond over 1000 times
        self.autoLoopTask = asyncio.create_task(self.loopServerUpdates())

    def _dataUpdated(self):
        self.lastUpdated = datetime.now().timestamp()


    async def loopServerUpdates(self):
        while self.running == True:
            oldUpdated =  self.lastUpdated

            await asyncio.to_thread(self._getInfo)
            await asyncio.to_thread(self._getPlayers)
            
            if self.failedRetries >= 200:
                self.delayedTimeout = 60

            if oldUpdated < self.lastUpdated:
                logging.info(f"Data has been auto-updated for {self.serverTuple}")
                if self.delayedTimeout == 60:
                    self.failedRetries = 0
                    self.delayedTimeout = 10

            await asyncio.sleep(self.delayedTimeout)     
    """
    Methods which update the server infromation
    """
    def _getInfo(self):
        try:
            info = a2s.info(self.serverTuple) # type: ignore
            self.info = ArmaInfo(
                name=info.server_name,
                players=info.player_count,
                maxPlayers=info.max_players,
                passwordProtected=info.password_protected,
                mapName=info.map_name
                )
            logging.info(f"Current information for {self.serverTuple} has been updated")
            self._dataUpdated()
            pass
        except BufferExhaustedError or TimeoutError:
            logging.error("Server is unable to respond to query",exc_info=True)
            self.failedRetries += 1
        except BrokenMessageError:
            logging.warning("Server failed to send a proper message",exc_info=True)
            self.failedRetries += 1
        except Exception as e:
            logging.warning(f"Server failed due to {e}",exc_info=True)
            self.failedRetries += 1    

    def _getPlayers(self):
        try:
            players = a2s.players(self.serverTuple) # type: ignore
            playerArray = []
            for player in players:
                _localplayer = Player(player.name,player.score,player.duration)
                playerArray.append(_localplayer)
            self.players = playerArray
            logging.info(f"Current player list for {self.serverTuple} has been updated")
            self._dataUpdated()
            pass
        except BufferExhaustedError or TimeoutError:
            logging.error("Server is unable to respond to query",exc_info=True)
            self.failedRetries += 1
        except BrokenMessageError:
            logging.warning("Server failed to send a proper message",exc_info=True)
            self.failedRetries += 1
        except Exception as e:
            logging.warning(f"Server failed due to {e}",exc_info=True)
            self.failedRetries += 1    