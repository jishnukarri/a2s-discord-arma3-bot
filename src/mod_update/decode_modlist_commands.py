from bs4 import BeautifulSoup as bs4
import discord
from discord.ext import commands, tasks
from discord import app_commands
import re
import requests
from src.mod_update.getSteamInformation import getModlistInformation


class Mod:
    def __init__(self, name: str, link: str, workshopID: int) -> None:
        self.name = name
        self.link = link
        self.workshopID = workshopID


class ProcessedModlist:
    def __init__(self, name: str, modlist: list[Mod]) -> None:
        self.name = name
        self.modlist = modlist
        self.modlist_size = len(self.modlist)


def decode_modlist(file: str) -> ProcessedModlist:

    s = bs4(file, "html.parser")
    name = ""
    get_name = s.find("meta", {"name": "arma:PresetName"})
    if get_name:
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
                getWorkshopID = int(getWorkshopID.group(1))
            else:
                getWorkshopID = 0
            mods.append(Mod(mod[0], mod[1], getWorkshopID))

    modlist = ProcessedModlist(name, mods)

    return modlist


# currently accessible to all users.
class ModUpdateReminder(app_commands.Group):
    def __init__(self, client: discord.Client) -> None:
        super().__init__(
            name="modlist_commands",
            description="Commands used to manage modlist reminders - mod updates",
        )
        self.client = client

    @app_commands.command(name="add_modlist", description="add your arma 3 modlist")
    @app_commands.describe(user_file="Drag and drop or select your file here")
    async def upload_file(
        self, interaction: discord.Interaction, user_file: discord.Attachment
    ):
        await interaction.response.defer(ephemeral=True)

        file_data = await user_file.read()
        modlist = decode_modlist(file_data.decode("utf-8"))
        mods = getModlistInformation(modlist.modlist)
        await interaction.followup.send(
            f"Received **{user_file.filename}** ({len(file_data)} bytes)"
        )
