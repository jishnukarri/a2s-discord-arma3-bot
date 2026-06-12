import discord
import datetime
from tabulate import tabulate


class Embeds:
    #Embed Functions
    leaderboardTitle = lambda title: f"{title}'s Leaderboard" if (title) else "Leaderboard"

    def __init__(self,title,footer,footer_icon):
        self.title = title
        self.footer = footer
        self.footer_icon = footer_icon
        
        
    def createLeaderboard(self,leaderboard:list) -> discord.Embed:
        """generates discord emebed

        Args:
            leaderboard (list): a list of tuples from sqliteDB from the 'database' DB

        Returns:
            discord.Embed: returns a discordEmebed
        """        
        
        table = {"Name":[],"Kills":[],"Time Played":[]}
        for row in leaderboard:
            table["Name"].append(row[0])
            table["Kills"].append(row[1])
            table["Time Played"].append(row[2])
        embed = discord.Embed(
            title=self.leaderboardTitle(self.title), #Lambda Function - Title
            timestamp=datetime.now())
        embed.add_field(name="",
                        value=f"""
                        ```md
                        {tabulate(table,headers="keys")}
                        ```
                        """)
        if (self.footer):
            embed.set_footer(text=self.footer,icon_url=self.footer_icon)
        return embed
    def createServerStatus(self,servers:list):
        pass