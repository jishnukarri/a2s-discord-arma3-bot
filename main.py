import src.bot as bot
from src.config import CLIENT_TOKEN
import src.logger as logger


logger.setup_logging()


DiscordClient = bot.DiscordBot()
DiscordClient.run(CLIENT_TOKEN)
