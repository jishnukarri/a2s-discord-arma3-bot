import os
import requests
from dotenv import load_dotenv


"""

LOCAL ENVIROMENT VARIBLES IMPORT

"""
load_dotenv()

CLIENT_TOKEN = os.getenv("CLIENT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
DATABASE_FILE = os.getenv("DATABASE_FILE")
RAW_REPO_LINK = os.getenv("RAW_REPO_LINK")
TITLE = os.getenv("TITLE")
FOOTER = os.getenv("FOOTER")
FOOTER_ICON = os.getenv("FOOTER_ICON")
