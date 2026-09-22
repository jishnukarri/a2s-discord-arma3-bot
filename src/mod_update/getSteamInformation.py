import requests
from src.config import CONFIG
import logging


hasSteamKey = True if CONFIG.STEAM_API_KEY != "NO_KEY_PROVIDED" else False


class SteamMod:
    def __init__(self, workshopID, icon, name, lastUpdated, size) -> None:
        self.id: int = workshopID
        self.icon: str = icon
        self.name: str = name
        self.lastUpdated: str = lastUpdated
        self.fileSize: int = size


def getWorkshopInformation(payload: dict) -> list[SteamMod] | None:
    steamMods = []

    workshopResponse = requests.post(
        "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/",
        data=payload,
    )

    if workshopResponse.ok:
        workshopResponse = workshopResponse.json()
    else:
        logging.warning("[STEAM-WORKSHOP] Workshop response failed")
        return None

    for modResponse in workshopResponse["response"]["publishedfiledetails"]:
        print(modResponse)
        _mod = SteamMod(
            modResponse.get("publishedfileid"),
            modResponse.get("preview_url"),
            modResponse.get("title"),
            modResponse.get("time_updated"),
            modResponse.get("file_size"),
        )
        steamMods.append(_mod)

    return steamMods


def getModlistInformation(modIDs) -> list[SteamMod] | bool:
    payload: dict[str, int | str] = {
        "itemcount": len(modIDs) - 1,
    }

    if hasSteamKey:
        payload["key"] = str(CONFIG.STEAM_API_KEY)

    for id, Mod in enumerate(modIDs):
        payload[f"publishedfileids[{id}]"] = Mod.workshopID
    response = getWorkshopInformation(payload)
    if response != None:
        return response
    else:
        return False