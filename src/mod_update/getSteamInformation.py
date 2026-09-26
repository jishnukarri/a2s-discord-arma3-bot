from src.mod_update import hasSteamKey
from src.data_models import SteamMod
import requests
import logging


def getWorkshopInformation(payload: dict) -> list[SteamMod] | None:
    steamMods = []

    workshopResponse = requests.post(
        "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/",
        data=payload,
    )

    if workshopResponse.ok:
        workshopResponse = workshopResponse.json()
    else:
        logging.warning(f"[STEAM-WORKSHOP] Workshop response failed - payload :- {payload} response:- {workshopResponse.__dict__}")
        return None

    for modResponse in workshopResponse["response"]["publishedfiledetails"]:
        logging.info(f"[STEAM-WORKSHOP] Processing {modResponse.get("title")}")
        if modResponse.get("title") == None:
            continue
        _mod = SteamMod(
            modResponse.get("publishedfileid"),
            modResponse.get("preview_url"),
            modResponse.get("title"),
            modResponse.get("time_updated"),
            modResponse.get("file_size"),
        )
        steamMods.append(_mod)
    logging.info(f"[STEAM-WORKSHOP] Processed all mods.")
    return steamMods

""" Modlist Information when a new Modlist is added """
def getModlistInformation(modIDs) -> list[SteamMod] | None:
    payload: dict[str, int | str] = {
        "itemcount": len(modIDs) - 1,
    }

    if hasSteamKey != False:
        logging.info(f"[STEAM-WORKSHOP] Steam key available.")
        payload["key"] = str(hasSteamKey)

    for id, Mod in enumerate(modIDs):
        payload[f"publishedfileids[{id}]"] = Mod.workshopID
    response = getWorkshopInformation(payload)
    if response != None:
        logging.info(f"[STEAM-WORKSHOP] Modlist information request sucessful.")
        return response
    else:
        logging.warning("[STEAM-WORKSHOP] Modlist information request failed.")
        return

""" Modlist Information for Reminder loops"""
def getModlistInformationLoop(modlist:list[SteamMod]) -> list[SteamMod] | None:
    payload: dict[str, int | str] = {
        "itemcount": len(modlist),
    }

    if hasSteamKey != False:
        logging.info(f"[STEAM-WORKSHOP] Steam key available.")
        payload["key"] = str(hasSteamKey)

    for id, Mod in enumerate(modlist):
        payload[f"publishedfileids[{id}]"] = Mod.id
    response = getWorkshopInformation(payload)
    if response != None:
        logging.info(f"[STEAM-WORKSHOP] Modlist information request sucessful.")
        return response
    else:
        logging.warning("[STEAM-WORKSHOP] Modlist information request failed.")
        return None