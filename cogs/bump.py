import discord
from discord.ext import commands


class Bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Bump(bot))
