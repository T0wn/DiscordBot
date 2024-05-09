import os
from DictatorBot import DictatorBot

BOT_TOKEN = os.getenv("BOT_TOKEN")
    
bot = DictatorBot()
bot.run(BOT_TOKEN)
