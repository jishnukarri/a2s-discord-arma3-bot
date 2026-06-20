# Discord Server Status Bot

This project is a2s discord bot which displays server status for a2s servers. It was specfially built for arma3 servers but it will work will most if not all a2s servers.

# Motivation
I previously built a vibe coded version of this but it was always buggy and it was more of a experiment which was used for a private community. At the start of my coding journey, I was quite reliant on ai to do everything but with experience and advice from people. I've learnt that AI is a great tool to so something faster but it cannot be the controller of the project. Since the old version was quite buggy and I decided to rebuild it myself with less ai usage and in the hopes of understanding the code of what i wrote.

# Install
Requirements: UV(python package manager), Python 3.14

* Clone Repository: ``` git clone https://codeberg.org/CarrotCereal124/a2s-discord-bot.git```
* Add Config for the Both: 
    1. Copy the `.env.example` and rename it as `.env`
    2. Go to [discord developer portal](https://discord.com/developers/applications) and get `CLIENT_TOKEN` and add it to the env file
    3. Get `GUILD_ID`,`CHANNEL_ID` from your discord client(enable developer mode to see details)
    4. `LOGGING_FILE`,`DATABASE_FILE`,`TITLE`,`FOOTER`,`FOOTER_ICON` - are local which can be decided by you
    5. `RAW_REPO_LINK` is the link to the server configration repo. Since this was built for a private community, a public-working repo link is set by default in the given .env

* Run the bot: ```uv run main.py```

# Example Screenshort

![Screenshort](/screenshort.png)

# Tested Games
Half-Life 2, Half-Life, Team Fortress 2, Counter-Strike: Global Offensive, Counter-Strike 1.6, ARK: Survival Evolved, Rust