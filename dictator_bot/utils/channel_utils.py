from enum import Enum, auto

from discord import Guild


class ChannelTypes(Enum):
    SHAME_CHANNEL = "Skammekroken"
    HORNYJAIL = "Hornyjail"

class VoiceAction(Enum):
    SHAME = auto()
    JAILSHAME = auto()
    REDEEM = auto()
    NOTHING = auto()


async def create_channel(guild: Guild, channel_name):
    return await guild.create_voice_channel(channel_name)


def channel_exists(channels, channel_id):
    t = next(filter(lambda channel: channel.id == channel_id, channels), None)
    return t is not None


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