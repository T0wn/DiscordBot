import discord
from asyncio import sleep

class DictatorBot(discord.Client):
    def __init__(self, skammekroken, verdilos):
        super().__init__()

        # variabelnavn in case man vil endre navnet på skammekroken kanalen eller verdiløs rollen. 
        self.skammekroken = skammekroken
        self.verdilos = verdilos

        # lagrer rollene til folk som er verdiløse, slik at de kan få de samme rollene tilbake igjen.
        self.shamedUsers = {}



    async def on_ready(self):
        print(f'Logged on as {self.user}')


    # Denne kjøres hver gang noe i voice kanalene endrer seg (mute, join, leave, etc..).
    async def on_voice_state_update(self, user, oldVoiceState, newVoiceState):
        if self.should_be_shamed(user, oldVoiceState, newVoiceState):
            await self.shame(user)
        elif self.should_be_redeemed(user, oldVoiceState, newVoiceState):
            await self.redeem(user)


    # sjekker om en bruker skal shames.
    def should_be_shamed(self, user, oldVoiceState, newVoiceState):
        if user != self.user:
            if oldVoiceState.channel and newVoiceState.channel:
                if (newVoiceState.channel.name == self.skammekroken and newVoiceState != oldVoiceState):
                    return True
        return False


    # sjekker om en bruker skal redeemes.
    def should_be_redeemed(self, user, oldVoiceState, newVoiceState):
        if user != self.user:
            if oldVoiceState.channel and newVoiceState.channel:
                if newVoiceState.channel.name != self.skammekroken and newVoiceState != oldVoiceState:
                    if newVoiceState.channel:
                        return True
        return False



    def add_shamed_user(self, user):
        userInfo = {'user': user, 'roles': user.roles}
        uid = f"{user.id} {user.guild.id}"
        self.shamedUsers[uid] = userInfo
        print(self.shamedUsers)



    def remove_shamed_user(self, user):
        uid = f"{user.id} {user.guild.id}"
        roles_to_assign = self.shamedUsers.pop(uid)['roles'][1:]
        print(self.shamedUsers)
        return roles_to_assign
        



    async def shame(self, user):
        # henter verdiløs rollen i serveren, hvis den finnes
        try:
            verdiloosRole = next(role for role in user.guild.roles if role.name == self.verdilos)
        except StopIteration:
            print("Exception: could not find verdiløs-role in guild")
        except Exception as e:
            print(e)
        
        # Lagrer brukeren og rollene han hadde før alle rollene blir fjerna.
        # Gir brukeren verdiløs rollen.
        self.add_shamed_user(user)
        await user.remove_roles(*user.roles[1:]) # bruker slicer til å fjerne everyone rollen fra listen. Den kan ikke fjernes fra brukere.
        await user.add_roles(verdiloosRole)

        # Connecter til voicechannel og spiller shame audio
        try:
            connection = await user.voice.channel.connect()
            audio = discord.FFmpegPCMAudio("./audio/shame-1.mp3")

            player = connection.play(audio)
            
            while connection.is_playing():
                await sleep(1)
            await connection.disconnect()
        except discord.errors.ClientException: # Denne kastes hvis boten allerede er connecta til voicechannelen, f.eks hvis vi kaster 2 personer i skammekroken etter hverandre.
            pass
        except Exception as e:
            print(e)

        

    async def redeem(self, user):
        # fjerner bruker infoen fra shamed users, og henter rollene som skal gies tilbake
        roles_to_assign = self.remove_shamed_user(user)
        await user.add_roles(*roles_to_assign)

        # henter verdiløs rollen i serveren, hvis den finnes
        try:
            verdiloosRole = next(role for role in user.guild.roles if role.name == self.verdilos)
        except StopIteration:
            print("Exception: could not find verdiløs-role in guild")
        except Exception as e:
            print(e)

        await user.remove_roles(verdiloosRole)