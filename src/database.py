import sqlite3
import os
import logging
import datetime

logger = logging.getLogger("database")


class BotDatabase:
    def __init__(self, database_file: str):
        logger.info(f"{database_file} - connecting to database")
        self.database = sqlite3.connect(database_file)
        self.cursor = self.database.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS database (player_name TEXT, kills INTEGER, playtime INTEGER, month TEXT, PRIMARY KEY (player_name, month))"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS messages (id INTEGER, leaderboard INTEGER, status INTEGER, PRIMARY KEY(id))"
        )
        self.cursor.execute(
            "INSERT OR IGNORE INTO messages(id, leaderboard, status) VALUES (1, 0, 0)"
        )
        self.database.commit()

    # Message Functions
    def getMessageID(self) -> dict:
        logger.info("getting message id")
        self.cursor.execute("SELECT leaderboard, status FROM messages WHERE id=1")
        messages = self.cursor.fetchone()
        if (messages[0] == 0) or (messages[1] == 0):
            logger.warning("no message id exists")
            messages = {"status": False}
            return messages
        else:
            logger.info(
                f"message id exists - leaderboard: {messages[0]}status:{messages[1]}"
            )
            messages = {"status": True,"leaderboard": messages[0], "statusMsg": messages[1]}
            return messages

    def updateMessageID(self, messages) -> None:
        if (messages.get("leaderboard") == 000) and (messages.get("statusMsg") == 000):
            logger.error(f"Message ID not returned in updateMessageID: {messages}")
        else:
            logger.info(
                f"Message ID updated - leaderboard: {messages.get("leaderboard")},status: {messages.get("statusMsg")}"
            )
            query = (
                "INSERT INTO messages(id,leaderboard,status) VALUES(1,?,?)"
                "ON CONFLICT(id) DO UPDATE SET leaderboard=?,status=?;"
            )
            self.cursor.execute(
                query, (messages.get("leaderboard"), messages.get("statusMsg"), messages.get("leaderboard"), messages.get("statusMsg"))
            )
            self.database.commit()

    ## Leaderboard Functions
    def getLeaderboard(self) -> list:
        self.cursor.execute("SELECT * FROM database")
        leaderboard = self.cursor.fetchall()
        return leaderboard

    def updateLeaderboard(
        self, player_name: str, kill_increase: int, playtimeIncrease: int
    ) -> None:
        current_month = datetime.datetime.now().strftime("%B-%Y")
        # this deals with both update value + creating a new row for the player every month
        self.cursor.execute(
            "INSERT INTO database(player_name, kills, playtime, month) VALUES(?,?,?,?)"
            "ON CONFLICT(player_name,month) DO UPDATE SET kills = kills + ?, playtime = playtime + ?;",
            (
                player_name,
                kill_increase,
                playtimeIncrease,
                current_month,
                kill_increase,
                playtimeIncrease,
            ),
        )
        self.database.commit()
