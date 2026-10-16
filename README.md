# Arma 3 Community Status Bot

A community discord bot which aims to help group admins to manage their Arma 3 Server(s)

## Description

This bot helps admins by allowing them to manage their modlist by sending them reminders when a mod updates, etc. This is done through using the SteamAPI interface(<b>CURRENTLY DOESN'NT SUPPORT PRIVATE/UNLISTED MODS</b>). It also helps to show a server status which allows players and admins to track thier current server status like number of people playing,kills and time played per player.


### Screenshots

![Screenshort  - Server Status](/screenshort1.png)
![Screenshort  - Mod Update Reminder Message](/screenshort2.webp)

## Getting Started

### Dependencies

* Python 3.14 or above
* [uv](https://docs.astral.sh/uv/) - Python package manager built in rust!!
* 
### Installing

* Download Python([which uv can do](https://docs.astral.sh/uv/guides/install-python/)) & [UV](https://docs.astral.sh/uv/#installation) from their offical sources   
* Clone Repository: ```git clone https://github.com/jishnukarri/a2s-discord-arma3-bot.git```
* Add Config for the Both: 
    1. Copy the `.env.example` and rename it as `.env`
    2. Go to [discord developer portal](https://discord.com/developers/applications) and get `CLIENT_TOKEN` and add it to the env file
    3. Get `GUILD_ID`,`CHANNEL_ID` from your discord client(enable developer mode to see details)
    4. `DATABASE_FILE` - is the file where all the information is stored
    6. `STEAM_API_KEY` is for mod update reminders
    7. Run ```uv run main.py``` to initlize the database and shut it down after 30s
    8. Edit the `DATABASE_FILE` file in the root folder of the project and run it!
* Run the bot: ```uv run main.py```

### Executing program

* Use a command line interface and type
```
cd ...\path\to\project
```
* Run the project initalisation script
```
uv sync
```
* Run the bot!
```
uv run main.py
```


## Help

<b>CURRENT ONLY SUPPORTS ARMA 3 - FUTURE WILL INCLUDE MORE STEAM GAMES</b>



## License

This project is licensed as per [LICENSE](/LICENSE.md).