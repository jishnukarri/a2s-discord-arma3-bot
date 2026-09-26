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

from dataclasses import dataclass


@dataclass
class Mod:
    def __init__(self, name: str, link: str, workshopID: int) -> None:
        self.name = name
        self.link = link
        self.workshopID = workshopID


@dataclass
class ProcessedModlist:
    def __init__(self, name: str, modlist: list[Mod]) -> None:
        self.name = name
        self.modlist = modlist
        self.modlist_size = len(self.modlist)


@dataclass
class SteamMod:
    def __init__(self, workshopID, icon, name, lastUpdated, size) -> None:
        self.id: int = workshopID
        self.icon: str = icon
        self.name: str = name
        self.lastUpdated: str = lastUpdated
        self.fileSize: int = size


@dataclass
class SteamStoreProcessedModlist:
    modlist: list[SteamMod]
    channelID:int
    roleID:int
