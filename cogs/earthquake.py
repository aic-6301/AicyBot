import discord
from discord.ext import commands, tasks
import json
from data import eewdata
import requests


class Earthquake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.eew_check.start()

    @tasks.loop(seconds=30)
    async def eew_check(self):
        with open('data/cache.json', 'r') as f:
            eventid = json.load(f)['eew_updatekey']
        url=requests.get('https://dev.narikakun.net/webapi/earthquake/post_data.json')
        response = url.json()
        if url.status_code == 200:
            if eventid != response['Head']['EventID']:
                if response['Body']['Intensity']['Observation']['MaxInt'] >= "4":
                    embed = await eewdata.eew_embed(response)
                    with open('data/channels.json', 'r') as f:
                        channel_id = int(json.load(f)['eew_4+_channels'])
                    channel = self.bot.get_channel(channel_id)
                    await channel.send(file=discord.File("./image.png"), embed=embed) # 登録済みチャンネルに送信
                    with open('data/cache.json', 'r') as f:  # idを保存
                            eew_updatekey = json.load(f)
                            eew_updatekey['eew_updatekey'] = response['Head']['EventID']
                    with open('data/cache.json', 'w') as f:
                            json.dump(eew_updatekey, f, indent=4)
                else:
                    embed = await eewdata.eew_embed(response)
                    with open('data/channels.json', 'r') as f:
                        channel_id = int(json.load(f)['eew_all_channels'])
                    channel = self.bot.get_channel(channel_id)
                    await channel.send(file=discord.File("./image.png"), embed=embed)
                    with open('data/cache.json', 'r') as f:  # idを保存
                        eew_updatekey = json.load(f)
                        eew_updatekey['eew_updatekey'] = response['Head']['EventID']
                    with open('data/cache.json', 'w') as f:
                        json.dump(eew_updatekey, f, indent=4)



async def setup(bot):
    await bot.add_cog(Earthquake(bot))
