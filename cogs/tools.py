import discord
from discord.ext import commands
from discord import app_commands
import requests
import os
from typing import Literal
import googlesearch


class tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



async def setup(bot):
    await bot.add_cog(tools(bot))
