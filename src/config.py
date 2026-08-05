from dotenv import load_dotenv
import json
import os
import logging
import sys
from functools import wraps

load_dotenv()
# Discord Secrets


""" Server Config's = Used to translate json into objects and backwards """


class MessageConfig:
    def __init__(self, statusMessageID: int = 0) -> None:
        self.statusMessageID: int = statusMessageID


class GuildConfig:
    def __init__(
        self,
        communityName: str = "",
        communityIcon: str = "",
        showUpdatedTimeStamp: bool = True,
    ) -> None:
        self.communityName = communityName
        self.communityIcon = communityIcon
        self.showUpdatedTimeStamp = showUpdatedTimeStamp


class ServerConfig:
    def __init__(self, ip, port: int) -> None:
        self.ip = ip
        self.port = port

def peristData(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if result is True:
            self.updateDB()
        return result
    return wrapper

class Database:
    def __init__(self, db_file: str) -> None:
        self.filePath = db_file
        self._loadDB()




    def _loadCleanDB(self,createWrite):
        self._saveDB(
            MessageConfig(),
            GuildConfig(),
            [ServerConfig("example.arma.com", 2303)],
            createWrite
        )
        logging.warning(
            "A Fresh copy has been created \n Restarting the bot to continue"
        )
        os.execv(sys.executable, [sys.executable] + sys.argv)

    """ Loads the DB into memory"""

    def _loadDB(self):
        if not os.path.exists(self.filePath):
            self._loadCleanDB("x")
        try:
            with open(self.filePath, "r") as DB:
                _db = json.load(DB)
                """
                Data being converted from JSON to Objects
                Objects will be stored seprately and be made gloabl DATABASE var
                """
                _guildData = _db["community_info"]
                _messageDATA = _db["messageIDs"]
                _serverData = _db["servers"]

                self.guildDATA = GuildConfig(**_guildData)
                self.messageDATA = MessageConfig(**_messageDATA)
                serversDATA = []
                for server in _serverData:
                    serversDATA.append(ServerConfig(**server))
                self.serversDATA = serversDATA
        except json.JSONDecodeError:
            logging.warning("DB Corrupted. Loading a new database")
            self._loadCleanDB("w")
        except Exception as e:
            logging.error("Unknown Error while loading DB.", exc_info=True)
            raise Exception("DB Error \n Check Logs")

    def _saveDB(self, _MConfig, _GConfig, _SsConfig,fileWrite="w"):
        try:
            db = {
                "community_info": _GConfig.__dict__,
                "messageIDs": _MConfig.__dict__,
                "servers": [server.__dict__ for server in _SsConfig],
            }
            with open(self.filePath, fileWrite) as DB:
                json.dump(db, DB)
        except Exception as e:
            logging.error("Unable to save to database file.", exc_info=True)
            raise Exception("Unable to save to database file.\nCheck logs.")

    def updateDB(self):
        try:
            db = {
                "community_info": self.guildDATA.__dict__,
                "messageIDs": self.messageDATA.__dict__,
                "servers": [server.__dict__ for server in self.serversDATA],
            }
            with open(self.filePath, "w") as DB:
                json.dump(db, DB)
        except Exception as e:
            logging.error("Unable to save to database file.", exc_info=True)
            raise Exception("Unable to save to database file.\nCheck logs.")

    
    @peristData
    def addServer(self,serverObject):
        if type(serverObject) == ServerConfig:
            self.serversDATA.append(serverObject)
            logging.info(f"new ServerObject added; {serverObject.__dict__} ")
            return True
        else:
            logging.error("Object could'nt be indentified")
            raise Exception("Object could'nt be identified")

    @peristData
    def removeServer(self,host:str,port:int):
        for serverObject in self.serversDATA:
            if (serverObject.ip == host) and (serverObject.host == port):
                self.serversDATA.remove(serverObject)
                logging.info(f"Server has been removed: {serverObject.__dict__}")
                return True
            else:
                logging.warning(f"Server could'nt be found: {serverObject.__dict__}")
                return False
    @peristData
    def updateCommunityData(self,cDATA):
        if type(cDATA) == GuildConfig:
            self.guildDATA = cDATA
            logging.info(f"Community Info has been updated: {cDATA.__dict__}")
            return True
        else:
            logging.warning(f"Community Info is not valid: {cDATA.__dict__}")
            return False
    @peristData
    def updateMessageID(self,newMessageID):
        if newMessageID != 0 and type(newMessageID) == int:
            self.messageDATA = MessageConfig(newMessageID)
            logging.info("Message ID in DB has been updated sucessfully")
            return True
        else:
            logging.error("Message ID is invalid;")
            return False
class Config:
    def __init__(self) -> None:
        self.CLIENT_TOKEN: str = str(os.getenv("CLIENT_TOKEN", ""))
        self.GUILD_ID: int = int(os.getenv("GUILD_ID", 0))
        self.CHANNEL_ID: int = int(os.getenv("CHANNEL_ID", 0))


_DATABASE_FILE: str = str(os.getenv("DATABASE_FILE"))

CONFIG = Config()

DATABASE = Database(_DATABASE_FILE)

GUILD_CONFIG = DATABASE.guildDATA
MESSAGE_CONFIG = DATABASE.messageDATA
SERVERS_CONFIG = DATABASE.serversDATA
