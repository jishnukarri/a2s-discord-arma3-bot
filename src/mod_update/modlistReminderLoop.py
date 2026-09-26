import asyncio
import logging

from src.config import DATABASE
from src.mod_update.getSteamInformation import getModlistInformationLoop
from src.mod_update import SteamMod, SteamStoreProcessedModlist

MOD_REMINDER_CHECK_TIMEOUT = 100

#todo: fix the fucking updated modkeys
async def modReminderLoop(name:str,values:SteamStoreProcessedModlist):
    while True:
        await asyncio.sleep(MOD_REMINDER_CHECK_TIMEOUT)
        logging.info(f"[MODLIST-LOOP] starting loop for {name}")
        logging.info("[MODLIST-LOOP] requesting data for all ")
        oldModlist = values.modlist
        updatedModlist = getModlistInformationLoop(values.modlist)
        logging.info("[MODLIST-LOOP] checking for updated mods")
        if updatedModlist is not None:
            oldModlistDict = {m.id: m for m in oldModlist}
            updatedModlistDict = {n.id: n for n in updatedModlist}

            _keys = oldModlistDict.keys() & updatedModlistDict.keys()

            # UPDATED MODS 
            _updated_mod_keys = []
            # checking if they got updated
            for id in _keys:
                if oldModlistDict[id].lastUpdated < updatedModlistDict[id].lastUpdated:
                    _updated_mod_keys.append(id)
            logging.info(f"[MODLIST-LOOP] loop completed sucessfully for {name}")
            payload = [True,{"newModlist":updatedModlist,"updatedModCount":len(_updated_mod_keys)-1,"updatedModIDs":_updated_mod_keys}]
            exstingData = DATABASE.guildDATA.serverModlists.get(name)
            if exstingData:
                dbPayload = SteamStoreProcessedModlist(
                    modlist=updatedModlist,
                    channelID=exstingData.channelID,
                    roleID=exstingData.roleID
                )
                DATABASE.modifyModlist(name,name,exstingData,dbPayload)
            return payload
        else:
            logging.info("[MODLIST-LOOP] steam failed to respond to query")
            return [None]