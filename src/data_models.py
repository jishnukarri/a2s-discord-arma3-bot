from dataclasses import dataclass
from dataclasses import dataclass


""" Database Scaffolds """


class MessageConfig:
    def __init__(self, statusMessageID: int = 0) -> None:
        self.statusMessageID: int = statusMessageID


class GuildConfig:
    def __init__(
        self,
        communityName: str = "",
        communityIcon: str = "",
        showUpdatedTimeStamp: bool = True,
        serverModlists:dict[str,SteamStoreProcessedModlist] = {}
    ) -> None:
        self.communityName = communityName
        self.communityIcon = communityIcon
        self.showUpdatedTimeStamp = showUpdatedTimeStamp
        self.serverModlists = serverModlists

class ServerConfig:
    def __init__(self, ip, port: int, name: str) -> None:
        self.ip = ip
        self.port = port
        self.name = name

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
    def __init__(self, name: str, score: int, time: str) -> None:
        self.name = name
        self.score = score
        self.time = time

    def __iter__(self):
        yield self.name
        yield self.score
        yield self.time

@dataclass
class Mod:
    name: str
    link: str
    workshopID: int


@dataclass
class ProcessedModlist:
    name:str
    modlist: list[Mod]
    modlist_size:int


@dataclass
class SteamMod:
    id: int
    icon: str
    name: str
    lastUpdated: str
    fileSize: int


@dataclass
class SteamStoreProcessedModlist:
    modlist: list[SteamMod]
    channelID:int
    roleID:int
