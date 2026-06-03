import a2s
import arma3query
import time
import logging

logging = logging.getLogger("a2s")

type serverTuple = tuple[str, int]

class a2sQuery():
    def __init__(self,serverTuple:serverTuple,rQuery:int,server_name:str):
        try:
            # if name not given; the server tuple acts as a name
            self.serverName = server_name or self.serverTuple
            self.serverTuple: serverTuple = serverTuple
            self.rQuery = rQuery
            self.serverInfo = [None,0]
            self.rules = [None,0]
        except TypeError:
            logging.error(f'SERVER_TUPLE FOR {serverTuple} has been configured incorrectly. \n Format : ("SERVER_HOST",SERVER_PORT)')
    def getServerInfo(self):
        if (time.time() - self.serverInfo[1] > 10):
            try:
                self.serverInfo[0] = a2s.info(self.serverTuple)
            except:
                logging.error(f'Unable to fetch server info for {self.serverTuple}')
            self.serverInfo[1] = time.time()
        return self.serverInfo[0]
    def getServerRules(self):
        if (time.time() - self.rules[1] > 10):
            try:
                self.rules[0] = arma3query.arma3rules(self.serverTuple)
            except:
                logging.error(f'Unable to fetch server rules for {self.serverTuple}')
            self.rules[1] = time.time()
        return self.rules[0]