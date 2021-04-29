import json
from DictatorBot import DictatorBot

with open('config.json') as file:
    config = json.load(file)

SKAMMEKROKEN = "Skammekroken"
VERDILOS = "Verdiløs"
    
bot = DictatorBot(SKAMMEKROKEN, VERDILOS)
bot.run(config['TOKEN'])