from discord.ext import commands
from discord.ext.commands import Context

from utils.channel_utils import *
from utils.data_utils import *


class DictatorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx: Context):
        await ctx.send(f'Hello {ctx.author.name}')

    @commands.command()
    async def setup(self, ctx: Context):
        guild: Guild = ctx.guild
        try:
            guild_config = load_guild_config(guild.id)
            if guild_config is None:
                skammekroken = await create_channel(guild, "Skammekroken")
                hornyjail = await create_channel(guild, "Hornyjail")
                set_guild_config(guild.id, {'skammekroken': skammekroken.id, 'hornyjail': hornyjail.id})
            else:
                if not channel_exists(ctx.guild.channels, guild_config["skammekroken"]):
                    guild_config["skammekroken"] = await create_channel(guild, "Skammekroken")
                if not channel_exists(ctx.guild.channels, guild_config["hornyjail"]):
                    guild_config["hornyjail"] = await create_channel(guild, "HornyJail")
                set_guild_config(guild.id, guild_config)
            await ctx.send("Setup complete!")

        except Exception as e:
            print(f"ex {e}")
            await ctx.send("Setup failed!")
