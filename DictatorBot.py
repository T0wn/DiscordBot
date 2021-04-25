from discord.py import Discord

class DictatorBot(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

TOKEN = "NzY3MTA0NTkwMTU1MjE5MDA2.X4tD0g.CRw4YM6Cw1VMiI9fc7Qibrnztkw"
bot = DictatorBot()
bot.run(TOKEN) 