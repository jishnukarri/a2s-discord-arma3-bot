import a2s
import arma3query
import time
import logging

logger = logging.getLogger("a2s")

type serverTuple = tuple[str, int]


class a2sQuery:
    def __init__(self, serverTuple: serverTuple, server_name: str):
        try:
            # if name not given; the server tuple acts as a name
            self.serverTuple: serverTuple = serverTuple
            self.serverName = server_name or self.serverTuple
            self.serverInfo = [None, 0]
            self.rules = [None, 0]
            self.players = None
        except TypeError:
            logger.error(
                f'SERVER_TUPLE FOR {serverTuple} has been configured incorrectly. \n Format : ("SERVER_HOST",SERVER_PORT)'
            )
            self.getServerInfo()

    def getServerInfo(self):
        if time.time() - self.serverInfo[1] > 10:
            try:
                self.serverInfo[0] = a2s.info(self.serverTuple)
            except Exception as e:
                logger.error(
                    f"Unable to fetch server info for {self.serverTuple} \n Error: {e}"
                )
            self.serverInfo[1] = (
                time.time()
            )  # This run wheter the query failed or not to avoid requests on servers which are offline
        return self.serverInfo[0]

    def getServerRules(self):
        if time.time() - self.rules[1] > 10:
            try:
                # check if server is arma3 to use arma3query
                if self.serverInfo[0].game == "Arma 3":
                    self.rules[0] = arma3query.arma3rules(self.serverTuple)
            except Exception as e:
                logger.error(
                    f"Unable to fetch server rules for {self.serverTuple} \n Errpr: {e}"
                )
            self.rules[1] = time.time()
        return self.rules[0]

    def getServerPlayers(self):
        try:
            self.players = a2s.players(self.serverTuple)
        except Exception as e:
            logger.error("Error getting players : {}".format(e))
            self.players = []
        return self.players
