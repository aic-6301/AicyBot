import discord
from discord.ext import commands
import requests
import json


class Botinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def ping(self, ctx, url=None):
        if ctx.invoked_subcommand is None:
            if url is None:
                url = requests.get(f"https://api.aic-group.net/get/ping?type=json")
                text = url.text
                data = json.loads(text)
                await ctx.send('ping値' + str(data['ping']) + f'\n' + 'ping先:' + (data['domain']))
            else:
                try:
                    url = requests.get(f"https://api.aic-group.net/get/ping?type=json&ip="+url)
                    text = url.text
                    data = json.loads(text)
                    await ctx.send('ping値' + str(data['ping']) + f'\n' + 'ping先:' + (data['domain']))
                except:
                    await ctx.send('URLが存在しません。別のURLを試してみて下さい')
    
    @ping.command()
    async def websocket(self, ctx, url=None):
        await ctx.send(f'pong!:ping_pong: {round(self.bot.latency * 1000)}ms')
        

async def setup(bot):
    await bot.add_cog(Botinfo(bot))
