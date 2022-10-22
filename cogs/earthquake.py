import discord
from discord.ext import commands, tasks
import json
from data import eewdata
import requests


class Earthquake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.eew_check.start()

    @tasks.loop(minutes=1)
    async def eew_check(self):
        with open('data/cache.json', 'r') as f:
            eew_updatekey = json.load(f)['eew_updatekey']
        request = requests.get("https://api.p2pquake.net/v2/history?codes=551&limit=1")
        response = request.json()[0]
        if (response['earthquake']['maxScale'] / 10) <= int(self.bot.config['notify_scale']):
            if request.status_code == 200:
                if eew_updatekey != response['id']:
                    channel_id = (977775289776095302)
                    channel = self.bot.get_channel(channel_id)
                    embed = eewdata.eew_embed(response)
                    await channel.send(embed=embed)
                    with open('data/cache.json', 'r') as f:
                        eew_updatekey = json.load(f)
                        eew_updatekey['eew_updatekey'] = response['id']
                    with open('data/cache.json', 'w') as f:
                        json.dump(eew_updatekey, f, indent=4)
            else:
                return

async def setup(bot):
    await bot.add_cog(Earthquake(bot))
