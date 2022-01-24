from discord.ext import commands


class DictatorCommands(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx, first):
        await ctx.send(f'hello {first}')