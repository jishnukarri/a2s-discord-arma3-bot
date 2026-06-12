import serverQuery
import arma3query
import time
import logging

logger = logging.getLogger("a2s")

type serverTuple = tuple[str, int]


class a2sQuery:
    def __init__(self, serverTuple: serverTuple, rQuery: int, server_name: str):
        try:
            # if name not given; the server tuple acts as a name
            self.serverTuple: serverTuple = serverTuple
            self.serverName = server_name or self.serverTuple
            self.rQuery = rQuery
            self.serverInfo = [None, 0]
            self.rules = [None, 0]
        except TypeError:
            logger.error(
                f'SERVER_TUPLE FOR {serverTuple} has been configured incorrectly. \n Format : ("SERVER_HOST",SERVER_PORT)'
            )

    def getServerInfo(self):
        if time.time() - self.serverInfo[1] > 10:
            try:
                self.serverInfo[0] = serverQuery.info(self.serverTuple)
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
                self.rules[0] = arma3query.arma3rules(self.serverTuple)
            except Exception as e:
                logger.error(
                    f"Unable to fetch server rules for {self.serverTuple} \n Errpr: {e}"
                )
            self.rules[1] = time.time()
        return self.rules[0]
