from enum import Enum

from discord.ext import commands
from dictator_bot import DictatorBot


class ChannelTypes(Enum):
    SHAME_CHANNEL = "Skammekroken"
    HORNYJAIL = "Hornyjail"


class DictatorCommands(commands.Cog):
    def __init__(self, bot: DictatorBot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx, first):
        await ctx.send(f'hello {first}')

    @commands.command()
    async def config(self, ctx, channel_type, new_channel_name):
        if channel_type == ChannelTypes.SHAME_CHANNEL.value:
            self.bot.skammekroken = new_channel_name
            await ctx.send(f'{ChannelTypes.SHAME_CHANNEL.value} renamed to {new_channel_name}!')
        elif channel_type == ChannelTypes.HORNYJAIL.value:
            self.bot.hornyjail = new_channel_name
            await ctx.send(f'{ChannelTypes.HORNYJAIL.value} renamed to {new_channel_name}!')
        else:
            await ctx.send('No channel with that name!')
