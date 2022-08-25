import discord
from discord.ext import commands
import requests


class Botinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def ping(self, ctx):
        await ctx.send(f'pong!:ping_pong: {round(self.bot.latency * 1000)}ms')
    
    @ping.command()
    async def _site(self, ctx, url: discord.abc):
        response = requests.get(f'https://aic-group.sytes.net/api/get/ping/{url}')
        await ctx.send(f'{response.text}')

async def setup(bot):
    await bot.add_cog(Botinfo(bot))
