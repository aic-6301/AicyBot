import datetime
import os
import random

import aiohttp
import discord
import pytz
from discord.ext import commands
from discord.ext.tasks import loop
timezone = pytz.timezone('UTC')



def to_min(time_delta):
    seconds = time_delta.seconds
    return seconds // 60

class money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.stage_check.start()
        self.stage_check = False



    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice_time_ch = self.bot.get_channel(1025370949840810044)
        voice_money_min = int('10')
        voice_money_max = int('100')
        voice_give_per = int('10')
        if member.bot:
            return
        if before.channel == None and not after.afk:
            await voice_time_ch.send(f'{member.id} {datetime.datetime.now(tz=timezone)}')
            return
        if not before.channel == None:
            if not before.afk and after.channel == None:
                async for msg in voice_time_ch.history():
                    if msg.content.startswith(str(member.id)):
                        await msg.delete()
                        splited = msg.content.split(' ', 1)
                        user_id = splited[0]
                        time = datetime.datetime.strptime(splited[1], '%Y-%m-%d %H:%M:%S.%f%z')
                        now = datetime.datetime.now(tz=timezone)
                        delta = now - time
                        min = to_min(delta)
                        money = '50'
                        async with aiohttp.ClientSession(headers=self.bot.ub_header) as session:
                            await session.patch(url=f'{self.bot.ub_url}{member.id}', json={'cash': (min // 10) * money, 'reason': f'ボイスチャット報酬({min}分)'})
                        return
        if after.afk and not before.channel == None:
            async for msg in voice_time_ch.history():
                if msg.content.startswith(str(member.id)):
                    await msg.delete()
                    splited = msg.content.split(' ', 1)
                    user_id = splited[0]
                    time = datetime.datetime.strptime(splited[1], '%Y-%m-%d %H:%M:%S.%f%z')
                    now = datetime.datetime.now(tz=timezone)
                    delta = now - time
                    min = to_min(delta)
                    money = random.randint(voice_money_min, voice_money_max)
                    async with aiohttp.ClientSession(headers=self.bot.ub_header) as session:
                        await session.patch(url=f'{self.bot.ub_url}{member.id}', json={'cash': (min // 10) * money, 'reason': f'ボイスチャット報酬({min}分)'})
                    return
        if not before.channel == None and not after.channel == None:
            if before.afk and not after.afk:
                await voice_time_ch.send(f'{member.id}が{datetime.datetime.now(tz=timezone)}にVCに参加')
                return
        if before.channel == None:
            if after.afk:
                return

    @commands.Cog.listener()
    async def on_stage_instance_create(self,stage_instance):
        if stage_instance.channel == self.bot.stage:
            self.stage_check = True
    
    @commands.Cog.listener()
    async def on_stage_instance_delete(self,stage_instance):
        if stage_instance.channel == self.bot.stage:
            self.stage_check = False
    
    @loop(minutes=10.0)
    async def stage_check(self):
        #configロード
        stage_money_min = '10'
        stage_money_max = '100'
        if self.stage_check == True:
            for member in self.bot.stage.members:
                if member.bot is False:
                    money = random.randint(stage_money_min, stage_money_max)
                    async with aiohttp.ClientSession(headers=self.bot.ub_header) as session:
                            await session.patch(url=f'{self.bot.ub_url}{member.id}', json={'cash':money, 'reason': f'ステージチャンネル報酬'})


async def setup(bot):
    await bot.add_cog(money(bot))
