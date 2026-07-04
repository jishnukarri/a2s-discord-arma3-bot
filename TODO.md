Log: I decided to rewrite it due to major issue which would take hours to debug and may still fail
Major Issue: Inconistent data sent from modules
¬ 27/06/2026


Log: Mostly rewrote a2sQuery - i learnt that i can use @propertry decorators gives live informaiton which im using to pull information into my both emebeding;
This is amazing since now i dont need no tasks in discord and everything is taken care of async in my query objects
but i do have a question on wheter doing src\bot\main.py:49 is gonna assign the decorator to the dict so it will auto update; if not ill probs use a system suggest by AI since i know nothing else than that.
But overall progress is going good; i also built  JSON based config system to avoid over complicating it and the bot can be simply restarted when the config is updated by the user.
I recently found infisical which has been a great tool i now dont need to worry about making sure my .env is using the right values since it takes care of it.
Gonna get this to a MVP stage this weekend and ship it. 
So on planning thought, i will use a folder called modlists/{} and just create a new array for storing that in the config to the right server name

¬ 02/07/26


Log:
Today, i worked on fixing my async functions to update information; It was a lot of debugging due to a bug being nested. Although it took a while to find and fix the error. It finally works
New Issue:
I was hoping to just create a dict serverInformation for the discord bot and at init i linked it to the queryObject and the goal of it was to self update but this wasnt happening so i tried creating a async function; it still doesnt run due to a discord HTTP error 
I did repeat my code multiple times to get it working which in my opnion is a bad idea but i will redo functions which i repeated myself in at the end when its working
## Plan

This bot is built for a Arma3 Communites
    - It shows server status (MVP)
        * Inital plan is to only support arma3 servers(MVP)
        * Add support to also show other servers
    - Mod Update Reminders from steamWorkshop(MVP)
        * Scrape using beautifulSoup or just use requests + regex
        * Setup a asyncio task to check regularly for updates
    - Give Link to modlist(MVP)
        * Send new users on request the modlist
    - Mod update reminders and modlist to new users will work one on one as both need a arma3 html modlist(MVP)
    - Plan events maybe? currently against it as tools like Apollo exist but a idea if everything else goes smoothly



### Discord Side of things
- 