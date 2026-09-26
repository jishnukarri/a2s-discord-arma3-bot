from src.config import CONFIG,DATABASE
from src.data_models import (
    Mod,
    ProcessedModlist,
    SteamMod,
    SteamStoreProcessedModlist,
)
import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import View, ChannelSelect, RoleSelect, Button, Modal, TextInput
import asyncio
import logging

modlist_loop_tasks = []

"""

Data Structures

"""

hasSteamKey = CONFIG.STEAM_API_KEY if CONFIG.STEAM_API_KEY != "NO_KEY_PROVIDED" else False

import src.mod_update.decodeModlistCommands as decodeModlistCommands
from src.mod_update.modlistReminderLoop import modReminderLoop
import src.mod_update.getSteamInformation as getSteamInformation


"""

Discord Veiw's for the prompts

"""
class RenameModlistModal(discord.ui.Modal, title="Rename Modlist"):
    newName = discord.ui.TextInput(label="New Modlist Name", placeholder="Enter new name here...\n If it requires no change press submit without changes.", required=False)

    def __init__(self, currentName, values):
        super().__init__()
        self.currentName = currentName
        self.values = values

        self.newName.default = self.currentName

    async def on_submit(self, interaction: discord.Interaction):
        if self.newName != "" or self.newName != self.currentName:
            DATABASE.modifyModlist(self.currentName,self.newName.value,self.values,self.values)
            await interaction.response.send_message(f"Modlist renamed from **{self.currentName}** to **{self.newName.value}**!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Modlist is still **{self.currentName}**.", ephemeral=True)

class AddModlistPrompt(discord.ui.View):
    def __init__(self,currentName:str,values:SteamStoreProcessedModlist):
        super().__init__(timeout=180)
        self.currentName = currentName
        self.values = values 

        # select channel
        self.channelSelect = ChannelSelect(
            placeholder="Select a notification channel for the reminder... ",
            channel_types=[discord.ChannelType.text]
        )
        self.channelSelect.callback = self.channelCallback

        self.roleSelect = RoleSelect(
            placeholder="Select a role which should be pinged when a mod update happens..."
        )
        self.roleSelect.callback = self.roleCallback

        self.rename_button = Button(label="Rename Modlist", style=discord.ButtonStyle.secondary)
        self.rename_button.callback = self.rename_callback

        self.add_item(self.channelSelect)
        self.add_item(self.roleSelect)
        self.add_item(self.rename_button)

    async def channelCallback(self,interaction:discord.Interaction):
        selectedChannel = self.channelSelect.values[0]
        old_value = self.values

        new_value = SteamStoreProcessedModlist(
            modlist=old_value.modlist,
            channelID=selectedChannel.id,
            roleID=old_value.roleID,
        )

        DATABASE.modifyModlist(
            self.currentName,
            self.currentName,
            old_value,
            new_value,
        )

        self.values = new_value
        await interaction.response.send_message(f"Channel set to {selectedChannel.mention}", ephemeral=True)
    async def roleCallback(self,interaction:discord.Interaction):
        selectedRoleID = self.roleSelect.values[0]
        old_value = self.values

        new_value = SteamStoreProcessedModlist(
            modlist=old_value.modlist,
            channelID=old_value.channelID,
            roleID=selectedRoleID.id,
        )

        DATABASE.modifyModlist(
            self.currentName,
            self.currentName,
            old_value,
            new_value,
        )

        self.values = new_value
        await interaction.response.send_message(f"Channel set to {selectedRoleID.mention}", ephemeral=True)
    async def rename_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RenameModlistModal(self.currentName, self.values))
             
"""

Discord Messaging COG

"""

class ModUpdateReminder(app_commands.Group):
    def __init__(self, client: discord.Client) -> None:
        super().__init__(
            name="modlist_commands",
            description="Commands used to manage modlist reminders - mod updates",
        )
        self.client = client

        # start modlist loop for exsting mods
        if DATABASE.guildDATA.serverModlists:
            for name, values in DATABASE.guildDATA.serverModlists.items():
                modlist_loop_tasks.append(asyncio.create_task(modReminderLoop(name,values,self.client)))

    @app_commands.command(name="add_modlist", description="add your arma 3 modlist")
    @app_commands.describe(user_file="Drag and drop or select your file here")
    async def upload_file(
        self, interaction: discord.Interaction, user_file: discord.Attachment
    ):
        await interaction.response.defer(ephemeral=True)

        file_data = await user_file.read()
        modlist = decodeModlistCommands.decode_modlist(file_data.decode("utf-8"))
        steamMods = getSteamInformation.getModlistInformation(modlist.modlist)
        if steamMods is not None:
            payload = SteamStoreProcessedModlist(
                modlist=steamMods,
                channelID=0,
                roleID=0
            )

            DATABASE.addModlist(modlist.name,payload)
            logging.info(f"[MODLIST-COG] Modlist {modlist.name} has been added")
            modlist_loop_tasks.append(asyncio.create_task(modReminderLoop(modlist.name, payload,self.client)))
            view = AddModlistPrompt(modlist.name,payload)
            await interaction.followup.send(
                f"Modlist has been added to the modReminder task. Please select the channel to send notifcations and the role to ping for updates.",
                view=view,
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"Please try later.\n Unable to process information due to steam API not responding.",
                ephemeral=True
            )