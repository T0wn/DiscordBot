import json
from DictatorBot import DictatorBot

with open('config.json') as file:
    config = json.load(file)

BOT_TOKEN = config['TOKEN']
SKAMMEKROKEN = "Skammekroken"
VERDILOS = "Verdiløs"
    
bot = DictatorBot(SKAMMEKROKEN, VERDILOS)
bot.run(BOT_TOKEN)