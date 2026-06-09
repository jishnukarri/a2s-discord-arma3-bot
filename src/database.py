import sqlite3
import os
import logging
import datetime
logging = logging.getLogger('database')


class BotDatabase:
    def __init__(self,database_file:str):
        logging.info(f'{database_file} - connecting to database')
        self.database = sqlite3.connect(database_file)
        self.cursor = self.database.cursor()
        if os.path.exists(database_file) != True:
            #leaderboard db
            self.cursor.execute('CREATE TABLE database (player_name TEXT, kills INTEGER,playtime INTEGER, month TEXT, PRIMARY KEY (player_name,month))')
            #message db
            self.cursor.execute('CREATE TABLE messages (id INTEGER, leaderboard INTEGER, status INTEGER, PRIMARY KEY(id))')
            self.cursor.execute("INSERT INTO messages(id,leaderboard,status) VALUES (1,000,000)")
        self.database.commit()

    # Message Functions
    def getMessageID(self) -> dict:
        logging.info("getting message id")
        self.cursor.execute('SELECT id=1 FROM messages')
        messages = self.cursor.fetchall()
        if (messages[1] == 000) or (messages[2] == 000):
            logging.warning("no message id exists")
            messages = {"status":False }
            return messages
        else:
            logging.info(f"message id exists - leaderboard: {messages[1]}status:{messages[2]}")
            messages = {"leaderboard":messages[1],"status":messages[2]}
            return messages
    def updateMessageID(self,messages) -> None:
        if (messages[1] == 000) and (messages[2] == 000):
            logging.error(f"Message ID not returned in updateMessageID: {messages}")
        else:
            logging.info(f"Message ID updated - leaderboard: {messages[1]},status: {messages[2]}")
            query = f"INSERT INTO messages(id,leaderboard,status) VALUES(1,{messages[1]},{messages[2]}) ON CONFLICT(id) DO UPDATE SET leaderboard={messages[1]},status={messages[2]};)"
            self.cursor.execute(query)
    
    ## Leaderboard Functions
    def getLeaderboard(self) -> list:
        self.cursor.execute("SELECT * FROM database")
        leaderboard = self.cursor.fetchall()
        return leaderboard
    def updateLeaderboard(self,player_name:str, kill_increase:int, playtimeIncrease:int) -> None:
        current_time = datetime.datetime.now().strftime("%B-%Y")
        # this deals with both update value + creating a new row for the player every month
        query = f"INSERT INTO database(player_name, kills, time, month) VALUES({player_name},{kill_increase}{playtimeIncrease},{current_time}) ON CONFLICT(player_name,month) DO UPDATE SET kills = kills + {kill_increase}, playtime = playtime + {playtimeIncrease};"
        self.cursor.execute(query)
    
