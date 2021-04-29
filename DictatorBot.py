import discord
from time import sleep

class DictatorBot(discord.Client):
    def __init__(self, skammekroken, verdilos):
        super().__init__()
        self.skammekroken = skammekroken
        self.verdilos = verdilos

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

    async def on_voice_state_update(self, user, oldVoiceState, newVoiceState):
        if self.should_be_shamed(user, oldVoiceState, newVoiceState):
            await self.shame(user)
        elif self.should_be_redeemed(user, oldVoiceState, newVoiceState):
            self.redeem(user)

    def should_be_shamed(self, user, oldVoiceState, newVoiceState):
        if user != self.user:
            if oldVoiceState.channel and newVoiceState.channel:
                if (newVoiceState.channel.name == self.skammekroken and newVoiceState != oldVoiceState):
                    return True
        return False

    def should_be_redeemed(self, user, oldVoiceState, newVoiceState):
        if user != self.user:
            if oldVoiceState.channel and newVoiceState.channel:
                if newVoiceState.channel.name != self.skammekroken and newVoiceState != oldVoiceState:
                    if newVoiceState.channel:
                        return True
        return False

    async def shame(self, user):
        def after(error):
            print(error)

        print("shaming")
        connection = await user.voice.channel.connect()
        audio = discord.FFmpegPCMAudio("./audio/shame-1.mp3")

        player = connection.play(audio, after=after )
        
        while connection.is_playing():
            sleep(1)
        await connection.disconnect()

    def redeem(self, user):
        print("redeeming")
        pass