import discord
import datetime
from tabulate import tabulate


class Embeds:

    # Embed Functions
    leaderboardTitle = lambda title: (
        f"{title}'s Leaderboard" if (title) else "Leaderboard"
    )


    statusTitle = lambda title: (
        f"{title}'s Server Status" if (title) else "Server Status"
    )


    def __init__(self, title, footer, footer_icon):
        self.title = title
        self.footer = footer
        self.footer_icon = footer_icon



    """createLeaderboard - generates discord leaderboard emebed for discordtasks

    Args:
        leaderboard (list): a list of tuples from sqliteDB from the 'database' DB

    Returns:
        discord.Embed: returns a discordEmebed
    """

    def createLeaderboard(self, leaderboard: list) -> discord.Embed:
        table = {"Name": [], "Kills": [], "Time Played": []}
        for row in leaderboard:
            table["Name"].append(row[0])
            table["Kills"].append(row[1])
            table["Time Played"].append(row[2])
        embed = discord.Embed(
            title=self.leaderboardTitle(self.title),  # Lambda Function - Title
            timestamp=datetime.now(),
        )
        embed.add_field(
            name="",
            value=f"""
                        ```md
                        {tabulate(table, headers="keys")}
                        ```
                        """,
        )
        if self.footer:
            embed.set_footer(text=self.footer, icon_url=self.footer_icon)
        return embed



    """createServerStatus - generates discord emebed used by discord tasks

    Args:
        servers (list): list with tuples of server data
    """

    def createServerStatus(self, servers) -> discord.Embed:
        # Format for the server display
        layout_name = "**{index}.{server}** - {current_players}/{all_players}"
        layout_body = """
        ```md
        {current_player_table}
        ```
        Last updated: {last_updated}
        """

        embed = discord.Embed(
            title=self.statusTitle(self.title), timestamp=datetime.now()
        )
        embed.add_field(
            name="ALL SERVER STATUS ARE UPDATED EVERY MINUTE", value="", inline=False
        )

        count = 0
        for server in servers:
            count = count + 1
            embed.add_field(
                name=layout_name.format(
                    index=count,
                    server=server.name,
                    current_players=server.current_players,
                    all_players=server.max_players,
                ),
                value=layout_body.format(
                    current_player_table=tabulate(server.player_table),
                    last_updated=server.last_updated
                ),
                inline=True
            )
            
        embed.footer(text=self.title)
        return embed