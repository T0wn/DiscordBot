import discord
import os
from asyncio import sleep

class DictatorBot(discord.Client):
    def __init__(self, skammekroken, verdilos):
        super().__init__()

        # variabelnavn in case man vil endre navnet på skammekroken kanalen eller verdiløs rollen. 
        self.skammekroken = skammekroken
        self.verdilos = verdilos

        # lagrer rollene til folk som er verdiløse, slik at de kan få de samme rollene tilbake igjen.
        self.shamedMembers = {}



    async def on_ready(self):
        print(f'Logged on as {self.user}')
        
        version = os.getenv("VERSION")
        if version is not None:
            activityVar = discord.Game(f"{version}")
            await self.change_presence(status=discord.Status.online, activity=activityVar)



    # Denne kjøres hver gang noe i voice kanalene endrer seg (mute, join, leave, etc..).
    async def on_voice_state_update(self, member, oldVoiceState, newVoiceState):
        if self.should_be_shamed(member, oldVoiceState, newVoiceState):
            await self.shame(member)
        elif self.should_be_redeemed(member, oldVoiceState, newVoiceState):
            await self.redeem(member)



    # sjekker om en bruker skal shames.
    def should_be_shamed(self, member, oldVoiceState, newVoiceState):
        if member != self.user:
            if oldVoiceState.channel and newVoiceState.channel:
                if (newVoiceState.channel.name == self.skammekroken and newVoiceState != oldVoiceState):
                    return True
        return False



    # sjekker om en bruker skal redeemes.
    def should_be_redeemed(self, member, oldVoiceState, newVoiceState):
        if member != self.user:
            if oldVoiceState.channel and newVoiceState.channel:
                if newVoiceState.channel.name != self.skammekroken and oldVoiceState.channel.name == self.skammekroken:
                    if newVoiceState.channel:
                        return True
        return False



    def add_shamed_member(self, member):
        memberInfo = {'user': member, 'roles': member.roles}
        uid = f"{member.id} {member.guild.id}"
        self.shamedMembers[uid] = memberInfo
        print(self.shamedMembers)



    def pop_shamed_member(self, member):
        uid = f"{member.id} {member.guild.id}"
        roles_to_assign = self.shamedMembers.pop(uid)['roles'][1:]
        print(self.shamedMembers)
        return roles_to_assign
        


    # henter verdiløs rollen i serveren, hvis den finnes
    def get_verdiloosRole(self, member):
        try:
            return next(role for role in member.guild.roles if role.name == self.verdilos)
        except StopIteration:
            raise StopIteration("could not find verdiløs-role in guild")



    async def shame(self, member):
        # henter verdiløs rollen i serveren, hvis den finnes
        verdiloosRole = self.get_verdiloosRole(member)
        
        # Lagrer brukeren og rollene han hadde før alle rollene blir fjerna.
        # Gir brukeren verdiløs rollen.
        self.add_shamed_member(member)
        await member.remove_roles(*member.roles[1:]) # bruker slicer til å fjerne everyone rollen fra listen. Den kan ikke fjernes fra brukere.
        await member.add_roles(verdiloosRole)

        # Connecter til voicechannel og spiller shame audio
        try:
            connection = await member.voice.channel.connect()
            audio = discord.FFmpegPCMAudio("./audio/shame-1.mp3")

            player = connection.play(audio)
            
            while connection.is_playing() and len(member.voice.channel.voice_states) > 1:
                await sleep(1)
            await connection.disconnect()
        except discord.errors.ClientException: # Denne kastes hvis boten allerede er connecta til voicechannelen, f.eks hvis vi kaster 2 personer i skammekroken etter hverandre.
            return
        except Exception as e:
            print(e)

        

    async def redeem(self, member):
        # fjerner bruker infoen fra shamed users, og henter rollene som skal gies tilbake
        roles_to_assign = self.pop_shamed_member(member)
        verdiloosRole = self.get_verdiloosRole(member)
        await member.add_roles(*roles_to_assign)
        await member.remove_roles(verdiloosRole)
