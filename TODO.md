Log: I decided to rewrite it due to major issue which would take hours to debug and may still fail
Major Issue: Inconistent data sent from modules
27/06/2026





## Plan

This bot is built for a Arma3 Communites
    - It shows server status (MVP)
        * Inital plan is to only support arma3 servers(MVP)
        * Add support to also show other servers
    - Mod Update Reminders from steamWorkshop
        * Scrape using beautifulSoup or just use requests + regex
        * Setup a asyncio task to check regularly for updates
    - Give Link to modlist
        * Send new users on request the modlist
    - Mod update reminders and modlist to new users will work one on one as both need a arma3 html modlist
    - Plan events maybe? currently against it as tools like Apollo exist but a idea if everything else goes smoothly



### Discord Side of things
- 