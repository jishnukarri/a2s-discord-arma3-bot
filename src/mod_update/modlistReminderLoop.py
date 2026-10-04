import asyncio
import logging
import discord
from aiohttp import ClientError as aiohttp_ClientError

from src.config import DATABASE
from src.mod_update.getSteamInformation import getModlistInformationLoop
from src.mod_update import SteamMod, SteamStoreProcessedModlist
MOD_REMINDER_CHECK_TIMEOUT = 100

async def sendModReminderMessage(channel:discord.TextChannel,message_value):
    try:
        message = await channel.send(message_value)
        logging.info(f"mod reminder message sent at {message.id}")
    except (discord.Forbidden):
        logging.error("Unable to edit due to permission error") 
    except (discord.HTTPException,aiohttp_ClientError,asyncio.TimeoutError) as e:
        logging.warning(f"Temporary error: Unable to edit message due to {e}")

async def sendModUpdateReminder(name:str,values:SteamStoreProcessedModlist,updatedModIDs:list[int],bot:discord.Client):
    """
    @Mention the Role : The following **mods** have been updated in the **modlist**:
    - Mod Name and link to steam workshop page
    """

    message = f"<@&{values.roleID}> The following **mods** have been updated in the **{name}**: \n"
    mods = {m.id: m for m in values.modlist}
    for id,modID in enumerate(updatedModIDs):
        _message = f"- [{mods[modID].name}](https://steamcommunity.com/sharedfiles/filedetails/?id={mods[modID].id}) \n"
        message = message + _message

    channel = bot.get_channel(values.channelID)
    if isinstance(channel, discord.TextChannel):
        message = await sendModReminderMessage(channel,message)
       
async def modReminderLoop(name:str,values:SteamStoreProcessedModlist,client:discord.Client):
    while True:
        try:
            logging.info(f"[MODLIST-LOOP] starting loop for {name}")
            logging.info("[MODLIST-LOOP] requesting data for all ")
            # Copy the previous state before querying; the fetched list becomes
            # the baseline for the next iteration.
            oldModlist = list(values.modlist)
            updatedModlist = await asyncio.to_thread(getModlistInformationLoop,oldModlist)
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
    
                exstingData = DATABASE.guildDATA.serverModlists.get(name)
                if exstingData:
                    dbPayload = SteamStoreProcessedModlist(
                        modlist=updatedModlist,
                        channelID=exstingData.channelID,
                        roleID=exstingData.roleID
                    )
                    if len(_updated_mod_keys) > 0:
                        await sendModUpdateReminder(name,dbPayload,_updated_mod_keys,client)
                    DATABASE.modifyModlist(name,name,exstingData,dbPayload)
                    values.modlist = updatedModlist
                else:
                    logging.info("[MODLIST-LOOP] steam failed to respond to query")
        except Exception as e:
            logging.exception(f"[MODLIST-LOOP] loop failed for {name}")
        await asyncio.sleep(MOD_REMINDER_CHECK_TIMEOUT)