from enum import Enum, auto

import discord
import os
import requests
import io
import asyncio
from PIL import Image
from discord.ext import commands
from dictatorcommands import DictatorCommands


class VoiceAction(Enum):
    SHAME = auto()
    JAILSHAME = auto()
    REDEEM = auto()
    NOTHING = auto()


class DictatorBot(commands.Bot):
    def __init__(self, skammekroken="Skammekroken", hornyjail="Hornyjail", verdilos="Verdiløs"):
        super().__init__(command_prefix="$")

        # variabelnavn in case man vil endre navnet på skammekroken kanalen eller verdiløs rollen.
        self.skammekroken = skammekroken
        self.verdilos = verdilos
        self.hornyjail = hornyjail

        # lagrer rollene til folk som er verdiløse, slik at de kan få de samme rollene tilbake igjen.
        self.shamedMembers = {}

        super().add_cog(DictatorCommands(self))

    async def on_ready(self):
        print(f'Logged on as {self.user}')

        version = os.getenv("VERSION")
        if version is not None:
            activity_var = discord.Game(f"{version}")
            await self.change_presence(status=discord.Status.online, activity=activity_var)

    # Denne kjøres hver gang noe i voice kanalene endrer seg (mute, join, leave, etc..).
    async def on_voice_state_update(self, member, old_voice_state, new_voice_state):
        action = self.get_action(member, old_voice_state, new_voice_state)
        if action == VoiceAction.SHAME:
            await self.shame(member)
        elif action == VoiceAction.JAILSHAME:
            await self.jail_shame(member)
        elif action == VoiceAction.REDEEM:
            await self.redeem(member)

    # sjekker om en bruker skal shames.
    def get_action(self, member, old_voice_state, new_voice_state):
        if member != self.user:
            if old_voice_state.channel and new_voice_state.channel:

                if new_voice_state != old_voice_state:
                    if new_voice_state.channel.name == self.skammekroken:
                        return VoiceAction.SHAME
                    if new_voice_state.channel.name == self.hornyjail:
                        return VoiceAction.JAILSHAME

                if new_voice_state.channel:
                    if new_voice_state.channel.name != self.skammekroken and old_voice_state.channel.name == self.skammekroken:
                        return VoiceAction.REDEEM
                    if new_voice_state.channel.name != self.hornyjail and old_voice_state.channel.name == self.hornyjail:
                        return VoiceAction.REDEEM

        return VoiceAction.NOTHING

    def add_shamed_member(self, member):
        member_info = {'user': member, 'roles': member.roles}
        uid = f"{member.id} {member.guild.id}"
        self.shamedMembers[uid] = member_info

    def pop_shamed_member(self, member):
        uid = f"{member.id} {member.guild.id}"
        roles_to_assign = self.shamedMembers.pop(uid)['roles'][1:]
        return roles_to_assign

    # henter verdiløs rollen i serveren, hvis den finnes
    def get_verdiloos_role(self, member):
        try:
            return next(role for role in member.guild.roles if role.name == self.verdilos)
        except StopIteration:
            raise StopIteration("could not find verdiloos-role in guild")

    async def set_member_verdiloos(self, member):
        # henter verdiløs rollen i serveren, hvis den finnes
        verdiloos_role = self.get_verdiloos_role(member)

        # Lagrer brukeren og rollene han hadde før alle rollene blir fjerna.
        # Gir brukeren verdiløs rollen.
        self.add_shamed_member(member)
        # bruker slicer til å fjerne everyone rollen fra listen. Den kan ikke fjernes fra brukere.
        await member.remove_roles(*member.roles[1:])
        await member.add_roles(verdiloos_role)

    async def shame(self, member):
        await self.set_member_verdiloos(member)

        # Connecter til voicechannel og spiller shame audio
        try:
            connection = await member.voice.channel.connect()
            audio = discord.FFmpegPCMAudio("./audio/shame-1.mp3")
            connection.play(audio)
            while connection.is_playing() and len(member.voice.channel.voice_states) > 1:
                await asyncio.sleep(1)
            await connection.disconnect()
        except discord.errors.ClientException:
            # Denne kastes hvis boten allerede er connecta til voicechannelen,
            # f.eks hvis vi kaster 2 personer i skammekroken etter hverandre.
            return
        except Exception as e:
            print(e)

    async def jail_shame(self, member):
        await self.set_member_verdiloos(member)

        avatar = Image.open(requests.get(member.avatar_url, stream=True).raw)
        avatar = avatar.resize((400, 400))

        meme_img = Image.open("images/meme.png")
        meme_img.paste(avatar, (900, 450))

        meme_img_byte_arr = io.BytesIO()
        meme_img.save(meme_img_byte_arr, format='PNG')
        meme_img_byte_arr.seek(0)
        img_send = discord.File(meme_img_byte_arr, filename="hornyjailmeme.png")

        await member.guild.system_channel.send(f"{member.mention}", file=img_send)

    async def redeem(self, member):
        # fjerner bruker infoen fra shamed users, og henter rollene som skal gies tilbake
        try:
            roles_to_assign = self.pop_shamed_member(member)
        except KeyError as e:
            print("Error: Could not find member among shamed members")
            return
        verdiloos_role = self.get_verdiloos_role(member)
        await member.add_roles(*roles_to_assign)
        await member.remove_roles(verdiloos_role)
