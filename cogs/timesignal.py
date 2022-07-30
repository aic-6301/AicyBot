from click import command


import discord
from discord.ext import commands


class Timesignal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

async def setup(bot):
    await bot.add_cog(Timesignal(bot))
