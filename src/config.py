from dotenv import load_dotenv
import json
import os
import logging
import sys
from functools import wraps
from src.data_models import (SteamMod, SteamStoreProcessedModlist,MessageConfig,GuildConfig,ServerConfig)

load_dotenv()
# Helpers

""" To save db when a function changes something"""


def peristData(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if result is True or result == "SAVED":
            self.updateDB()
        return result

    return wrapper

# this was from ai; pretty much to solve this db problem
def dict_to_object(data, cls):
    """
    Recursively turns a dictionary back into a class instance.
    """
    if isinstance(data, dict):
        # Create an empty instance of the target class without calling __init__ blocking checks
        obj = cls.__new__(cls)
        
        for key, value in data.items():
            # Get the expected type/class of the attribute if it's a sub-class
            # This looks at your class type hints if you use them, or you can check manually
            attr_type = getattr(cls, '__annotations__', {}).get(key, None)
            
            if isinstance(value, dict) and attr_type and hasattr(attr_type, '__dict__'):
                # Recursively build the nested inner class
                setattr(obj, key, dict_to_object(value, attr_type))
            elif isinstance(value, list) and attr_type and hasattr(attr_type, '__args__'):
                # Handle lists of custom objects if type hinted
                sub_cls = attr_type.__args__[0]
                setattr(obj, key, [dict_to_object(item, sub_cls) for item in value])
            else:
                setattr(obj, key, value)
        return obj
    return data


class Database:
    def __init__(self, db_file: str) -> None:
        self.filePath = db_file
        self._loadDB()

    """ Create a empty copy of a DB"""

    def _loadCleanDB(self, createWrite):
        self._saveDB(
            MessageConfig(),
            GuildConfig(),
            [],
            createWrite,
        )
        logging.warning(
            "A Fresh copy has been created \n Restarting the bot to continue"
        )
        os.execv(sys.executable, [sys.executable] + sys.argv)

    """ Loads the DB into memory """

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

                self.guildDATA = dict_to_object(_guildData, GuildConfig)
                loadedModlists = {}
                for name, rawModlist in self.guildDATA.serverModlists.items():
                    if isinstance(rawModlist, str):
                        rawModlist = json.loads(rawModlist)

                    if isinstance(rawModlist, dict):
                        rawModlist["modlist"] = [
                            dict_to_object(mod, SteamMod)
                            for mod in rawModlist.get("modlist", [])
                        ]
                        loadedModlists[name] = dict_to_object(
                            rawModlist, SteamStoreProcessedModlist
                        )
                    else:
                        loadedModlists[name] = rawModlist

                self.guildDATA.serverModlists = loadedModlists
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

    """ Converts all the objects back into json to save to file. """

    def _saveDB(self, _MConfig, _GConfig, _SsConfig, fileWrite="w"):
        try:
            db = {
                "community_info": _GConfig.__dict__,
                "messageIDs": _MConfig.__dict__,
                "servers": [server.__dict__ for server in _SsConfig],
            }
            fileName = self.filePath + '.tmp'
            with open(fileName, fileWrite) as DB:
                json.dump(db, DB, default=lambda obj: obj.__dict__)
            os.replace(fileName,self.filePath)
        except Exception as e:
            logging.error("Unable to save to database file.", exc_info=True)
            raise Exception("Unable to save to database file.\nCheck logs.")

    """ uses _saveDB to update the file with the latest data from memory"""

    def updateDB(self):
        self._saveDB(self.messageDATA, self.guildDATA, self.serversDATA)

    """ Adds a server to in-memory database"""

    @peristData
    def addServer(self, serverObject):
        if type(serverObject) == ServerConfig:
            self.serversDATA.append(serverObject)
            logging.info(f"new ServerObject added; {serverObject.__dict__} ")
            return True
        else:
            logging.error("Object could'nt be indentified")
            raise Exception("Object could'nt be identified")

    """ Removes a server to in-memory database"""

    @peristData
    def removeServer(self, host: str, port: int):
        for serverObject in self.serversDATA:
            if (serverObject.ip == host) and (serverObject.host == port):
                self.serversDATA.remove(serverObject)
                logging.info(f"Server has been removed: {serverObject.__dict__}")
                return True
            else:
                logging.warning(f"Server could'nt be found: {serverObject.__dict__}")
                return False

    """ Updates any changes to the guild's"""

    @peristData
    def updateCommunityData(self, cDATA):
        if type(cDATA) == GuildConfig:
            self.guildDATA = cDATA
            logging.info(f"Community Info has been updated: {cDATA.__dict__}")
            return True
        else:
            logging.warning(f"Community Info is not valid: {cDATA.__dict__}")
            return False

    """Verify Modlist data being recived"""
    def checkModlistParms(self,name,values) -> bool:
        if name != "" and type(values) == SteamStoreProcessedModlist:
            return True
        else:
            return False
    
    """ Allows to modify modlists"""
    @peristData
    def addModlist(self,name:str,values:SteamStoreProcessedModlist):
        if not self.checkModlistParms(name,values):
            logging.error(f"MOD DETAILS INVALID: {locals()} in addModlist")
            return "INVALID"
        currentGuild = self.guildDATA

        if name in currentGuild.serverModlists:
            logging.warning("MOD DETAILS NOT EXISTING in addModlist")
            return "EXSTING"

        currentGuild.serverModlists[name] = values
        self.guildDATA = currentGuild
        return "SAVED"

    """ Modify a exsting modlist"""
    @peristData
    def modifyModlist(self,oldName:str,newName:str,oldValues:SteamStoreProcessedModlist,newValues:SteamStoreProcessedModlist):
        if not self.checkModlistParms(oldName, oldValues):
            logging.error("Invalid old modlist data")
            return "INVALID"

        if not self.checkModlistParms(newName, newValues):
            logging.error("Invalid new modlist data")
            return "INVALID"

        currentGuild = self.guildDATA

        if oldName not in currentGuild.serverModlists:
            logging.warning(f"MOD DETAILS NOT EXISTING: {oldName} in modifyModlist")
            return "EXSTING"
        if currentGuild.serverModlists[oldName] == oldValues:
            currentGuild.serverModlists.pop(oldName)
            currentGuild.serverModlists[newName] = newValues
        else:
            if currentGuild.serverModlists[oldName] != oldValues:
                logging.error(
                    "MODLIST NOT UPDATED: old values do not match stored values"
                )
                return "NOT_MATCHING"
            logging.error("MODLIST NOT UPDATED DUE OLD MODLIST NOT MATCHING DICT in modifyModlist")

        self.guildDATA = currentGuild
        return "SAVED"

    """ Delete a existing modlist"""
    @peristData
    def deleteModlist(self,name:str,values:SteamStoreProcessedModlist):
        if not self.checkModlistParms(name,values):
            logging.error(f"MOD DETAILS INVALID: {locals()} in deleteModlist")
            return "INVALID"
        currentGuild = self.guildDATA

        if name not in currentGuild.serverModlists:
            logging.warning(f"MOD DETAILS NOT EXISTING: {name} in deleteModlist")
            return "EXSTING"
        if currentGuild.serverModlists[name] == values:
            currentGuild.serverModlists.pop(name)
        else:
            logging.error("modlist not deleted due modlist not matching object in deleteModlist")

        self.guildDATA = currentGuild
        return "SAVED"

    """ Updates message ID when a new message is sent"""

    @peristData
    def updateMessageID(self, newMessageID):
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
        self.STEAM_API_KEY: str = str(os.getenv("STEAM_API_KEY", "NO_KEY_PROVIDED"))


_DATABASE_FILE: str = str(os.getenv("DATABASE_FILE"))

CONFIG = Config()

DATABASE = Database(_DATABASE_FILE)
