from dotenv import load_dotenv
import json
import os
import logging


load_dotenv()
# Discord Secrets

CLIENT_TOKEN: str = str(os.getenv("CLIENT_TOKEN", ""))
GUILD_ID: int = int(os.getenv("GUILD_ID", 0))
CHANNEL_ID: int = int(os.getenv("CHANNEL_ID", 0))

# config file
DATABASE_FILE: str = str(os.getenv("DATABASE_FILE"))

DATABASE_CONFIG = {}
if os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE, "r+") as file:
        if file.read() == "":
            file.write("{}")
    with open(DATABASE_FILE, "r") as file:
        DATABASE_CONFIG = json.load(file)
else:
    logging.error(f"{DATABASE_FILE} not found in the given path")


"""
Functions to add to DATABASE
"""


def addToDatabase(keys: list, value: int) -> bool:
    if (keys == []) or (value == ""):
        logging.error("no key or value given")
        return False
    with open(DATABASE_FILE, "w") as file:
        try:
            current = DATABASE_CONFIG or {}
            if len(keys) > 1:
                for key in keys[:-1]:
                    if key not in current:
                        current[key] = {}
                    initKey = key
                    current[initKey][keys[-1]] = value
            else:
                current[keys[len(keys) - 1]] = value

            json.dump(current, indent=4, fp=file)
            logging.info("Data added to config", current)
            return True
        except Exception as e:
            logging.error("Unable to add data to Config", exc_info=True)
            return False
