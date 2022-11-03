import discord
from discord.ext import commands, tasks
import json
import requests
from datetime import datetime

class Alart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.alart.start()

    @tasks.loop(seconds=6)
    async def alart(self):
        with open('data/alart.json', 'r') as f:
            alart_link = json.load(f)['link']
        request = requests.get(f"https://api.aic-group.net/get/alert")
        text =request.text
        data = json.loads(text)
        if data['channel']['item'][0]['link'] != alart_link:
            time = datetime.strptime(data['channel']['item'][0]['pubDate'], '%a, %d %b %Y %H:%M:%S %z').strftime('%Y/%m/%d %H:%M:%S')
            embed=discord.Embed(title=data['channel']['item'][0]['title'], description=data['channel']['item'][0]['description'], color=discord.Colour.from_rgb(160, 106, 84))
            embed.set_footer(text=time)
            await self.bot.get_channel(949560203886604293).send(embed=embed)
            with open('data/alart.json', 'r') as f:
                alart_link_ = json.load(f)
                alart_link_['link'] = data['channel']['item'][0]['link']
            with open('data/alart.json', 'w') as f:
                json.dump(alart_link_, f, indent=4)


    async def cog_unload(self):
            self.alart.stop()

async def setup(bot):
    await bot.add_cog(Alart(bot))