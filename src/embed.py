import discord
import datetime
from tabulate import tabulate
#Universal Lamda Functions
title = lambda title: f"{title}'s Leaderboard" if (title) else "Leaderboard"


"""
Discord Embeds 

createLeaderboard 
parms: leaderboard:list, config: dict -> DiscordEmbed
"""

def createLeaderboard(leaderboard:list, config:dict) -> discord.Embed:
    
    table = {"Name":[],"Kills":[],"Time Played":[]}
    for row in leaderboard:
        table["Name"].append(row[0])
        table["Kills"].append(row[1])
        table["Time Played"].append(row[2])
    embed = discord.Embed(
        title=title(config['title']), #Lambda Function - Title
        timestamp=datetime.now())
    embed.add_field(name="",
                    value=f"""
                    ```md
                    {tabulate(table,headers="keys")}
                    ```
                    """)
    if (config.get('footer')):
        embed.set_footer(text=config.get('footer').text,icon_url=config.get('footer').image)
    return embed