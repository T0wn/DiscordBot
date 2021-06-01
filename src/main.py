from get_docker_secret import get_docker_secret

from DictatorBot import DictatorBot

BOT_TOKEN = get_docker_secret("bot_token")
SKAMMEKROKEN = "Skammekroken"
VERDILOS = "Verdiløs"
    
bot = DictatorBot(SKAMMEKROKEN, VERDILOS)

try:
    bot.run(BOT_TOKEN)
except AttributeError as e:
    print("ERROR: No bot_token secret found")
    exit(1)
except Exception as e:
    print(e)
    exit(1)