from src.data_models import ProcessedModlist, Mod
from bs4 import BeautifulSoup as bs4
import re
import logging

def decode_modlist(file: str) -> ProcessedModlist:

    s = bs4(file, "html.parser")
    name = ""
    get_name = s.find("meta", {"name": "arma:PresetName"})
    if get_name:
        logging.info("[MODLIST-DECODE] Preset name found")
        name = str(get_name.get("content"))
    modlistTable = s.select_one("div.mod-list table")

    mods = []
    if modlistTable:
        for r in modlistTable.find_all("tr"):
            mod = [
                c.get_text(strip=True)
                for c in r.find_all("td")
                if c.get_text(strip=True) != "Steam"
            ]
            getWorkshopID = re.search(r"id=(\d+)", mod[1])
            if getWorkshopID:
                logging.info("[MODLIST-DECODE] workshopID found.")
                getWorkshopID = int(getWorkshopID.group(1))
            else:
                logging.warning("[MODLIST-DECODE] workshopID not found")
                getWorkshopID = 0
            mods.append(Mod(mod[0], mod[1], getWorkshopID))

    modlist = ProcessedModlist(name, mods)

    return modlist