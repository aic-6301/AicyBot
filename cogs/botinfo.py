import discord
from discord.ext import commands
import requests
import json


class Botinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def ping(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'pong!:ping_pong: {round(self.bot.latency * 1000)}ms')
    
    @ping.command()
    async def site(self, ctx):
        url = requests.get(f"https://aic-group.sytes.net/api/get/ping/?type=json")
        text = url.text
        data = json.loads(text)
        await ctx.send('ping値' + str(data['ping']) + f'\n' + 'ping先:' + (data['domain']))

async def setup(bot):
    await bot.add_cog(Botinfo(bot))
