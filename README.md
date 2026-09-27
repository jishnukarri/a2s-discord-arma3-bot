# Discord Server Status Bot

This project is a2s discord bot which displays server status for a2s servers. It was specfially built for arma3 servers(this version only supports arma3servers)

# Install
Requirements: UV(python package manager), Python 3.14

* Clone Repository: ``` git clone https://github.com/jishnukarri/a2s-discord-arma3-bot.git```
* Add Config for the Both: 
    1. Copy the `.env.example` and rename it as `.env`
    2. Go to [discord developer portal](https://discord.com/developers/applications) and get `CLIENT_TOKEN` and add it to the env file
    3. Get `GUILD_ID`,`CHANNEL_ID` from your discord client(enable developer mode to see details)
    4. `DATABASE_FILE` - is the file where all the information is stored
    6. `STEAM_API_KEY` is for mod update reminders
    7. Run ```uv run main.py``` to initlize the database and shut it down after 30s
    8. Edit the `DATABASE_FILE` file and its done!
* Run the bot: ```uv run main.py```

# Example Screenshort

![Screenshort  - Server Status](/screenshort1.png)
![Screenshort  - Mod Update Reminder Message](/screenshort2.webp)

# Tested Games
Arma 3 **ONLY**

# Motivation
<del> I previously built a vibe coded version of this but it was always buggy and it was more of a experiment which was used for a private community. At the start of my coding journey, I was quite reliant on ai to do everything but with experience and advice from people. I've learnt that AI is a great tool to so something faster but it cannot be the controller of the project. Since the old version was quite buggy and I decided to rebuild it myself with no ai and in hopes of learning more of python and how to design the structre of the code..</del> <br>
However, since the idea changed a bittt from fixing the old bot to making a server management bot... The reasson is <b>I LOVE ARMA 3 😭</b> and from my experience of setting up multiple servers is that everyone wants to see if the servers up and everytime i had to do that. It was either that i had to go onto the server and check or use a free bot like Game Server Status which is very general and updates like maybe every 5 mins and it doesnt offer specfic features to arma 3 like modlist reminders etc. i meann stuff exist for it but its all over the place and this just gets it all into one...

:) hope it helps