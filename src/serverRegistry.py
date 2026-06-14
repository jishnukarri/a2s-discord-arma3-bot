import requests
import logging
from src.config import RAW_REPO_LINK

logger = logging.getLogger("serverRegistry")


class Mod:
    """
    This class is used to track mods that are pulled from github. Since they are multiple files with diffrent sets of data this is used to combine all data into one
    """

    def __init__(self, name, mod_link, steam):
        self.name = name
        self.mod_link = mod_link
        self.steam = steam


class serverRegistry:
    def __init__(self):
        self.active_servers = {}
        self.mod_dictonary = {}
        self.fetch_map_servers()
        
    def fetch_map_servers(self):
        try:
            content_file = requests.get(f"{RAW_REPO_LINK}/content.json").json()
            servers_file = requests.get(f"{RAW_REPO_LINK}/servers.json").json()
            steam_file = requests.get(f"{RAW_REPO_LINK}/steam.json").json()

            registry = {}

            # Active Servers
            for server_name, server_data in servers_file.items():
                # On the current system, mods are not updated and left untouched, so it will use the arma3query to pull mod infromation

                # mods = {}
                # for mod_name in server_data["mods"]:
                #     link = content_file.get("mods",{}).get(mod_name) or content_file.get("optionals",{}).get(mod_name) or content_file.get("dlc",{}).get(mod_name).get("link")
                #     steam = steam_file.get("mods",{}).get(mod_name)
                #     mod = Mod(mod_name,link,steam)
                #     mods.append(mod)
                registry[server_name] = {
                    "address": server_data.get("address"),
                    "port": server_data.get("port"),
                    "country": server_data.get("country"),
                    # "mods": mods
                }
            self.active_servers = registry

            # Mods
            mod_dictonary = {}
            for name, id in steam_file.items:
                link = (
                    content_file.get("mods", {}).get(name)
                    or content_file.get("optionals", {}).get(name)
                    or content_file.get("dlc", {}).get(name).get("link")
                )
                mod_dictonary[id] = {"name": name, "link": link}
            self.mod_dictonary = mod_dictonary
            logger.info("Rebuilt Github Server Data Cache")

        except Exception as e:
            logger.error(f"Failed to read maps from GitHub: {e}")
