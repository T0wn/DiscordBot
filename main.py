import json
from get_docker_secret import get_docker_secret
from discord.errors import LoginFailure

from DictatorBot import DictatorBot

BOT_TOKEN = get_docker_secret("bot_token")
SKAMMEKROKEN = "Skammekroken"
VERDILOS = "Verdiløs"
    
bot = DictatorBot(SKAMMEKROKEN, VERDILOS)

try:
    bot.run(BOT_TOKEN)
except AttributeError:
    print("ERROR: Invalid bot-token.")
    exit(1)
except LoginFailure:
    print("ERROR: Improper token has been passed")
    exit(1)
except Exception as e:
    print(e)
    exit(1)