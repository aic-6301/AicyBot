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
    async def eew_check(self, message):
        with open('data/cache.json', 'r') as f:
            eventid = json.load(f)['eew_updatekey']
        url=requests.get('https://dev.narikakun.net/webapi/earthquake/post_data.json')
        response = url.json()
        if requests.status_code == 200:
            if eventid != response['Head']['EventID']:
                if response['Body']['Intensity']['Observation']['MaxInt'] <= 4:
                    embed = eewdata.eew_embed(response)
                    with open('data/channels.json', 'r') as f:
                        channel_id = int(json.load(f)['eew_4+_channel'])
                    for channel in self.bot.get_all_channels(): # 登録チャンネルを探す
                        if channel.id in channel_id:
                            if channel == message.channel:
                                continue
                            await channel.send(embed=embed) # 登録済みチャンネルに送信
                            with open('data/cache.json', 'r') as f:  # idを保存
                                eew_updatekey = json.load(f)
                                eew_updatekey['eew_updatekey'] = response['id']
                            with open('data/cache.json', 'w') as f:
                                json.dump(eew_updatekey, f, indent=4)
                else:
                    embed = eewdata.eew_embed(response)
                    with open('data/channels.json', 'r') as f:
                        channel_id = int(json.load(f)['eew_all_channel'])
                    for channel in self.bot.get_all_channels(): # 登録チャンネルを探す
                        if channel.id in channel_id:
                            if channel == message.channel:
                                continue
                            await channel.send(embed=embed)
                            with open('data/cache.json', 'r') as f:  # idを保存
                                eew_updatekey = json.load(f)
                                eew_updatekey['eew_updatekey'] = response['id']
                            with open('data/cache.json', 'w') as f:
                                json.dump(eew_updatekey, f, indent=4)



async def setup(bot):
    await bot.add_cog(Earthquake(bot))
