import discord
from discord.ext import commands, tasks
from datetime import datetime
import asyncio


class Timesignal(commands.Cog):
    def __init__(self, bot):
        self.timesignal.start()
        self.bot = bot
        self.message = None
        self.embed = None

    @tasks.loop(seconds=10)
    async def timesignal(self):
        dt_now = datetime.now().strftime('%H')
        if datetime.now().strftime('%M') == '00':
            self.embed = discord.Embed(title='時報', colour=discord.Colour(0x4b78e6), description=f'{dt_now}時ちょうどをお知らせします')
            if dt_now == 0:
                self.embed.add_field(name='あけおめ!!', value=f'今日は{dt_now.month}/{dt_now.day}です')
            elif dt_now == 6:
                self.embed.add_field(name='おはよう!!',value='ニュースはa!newsで見れるぞ')
            elif dt_now == 12:
                self.embed.add_field(name='お昼だよ!!', value='ご飯を食べよう!!!')
            elif dt_now == 15:
                self.embed.add_field(name='お菓子の時間!!', value='お菓子を食べよう!!')
            elif dt_now == 18:
                self.embed.add_field(name='夜ごはん!!', value='夜ご飯を食べよう!!!')
            elif dt_now == 23:
                self.embed.add_field(name='夜だよ!!', value='そろそろねよう!!!')
        elif datetime.now().strftime('%M') == '30':
            self.embed = discord.Embed(title='時報', colour=discord.Colour(0x4b78e6), description=f'{dt_now}時30分をお知らせします')
        await asyncio.sleep(30)


        if self.embed != None:
            if self.message != None:
                await self.message.delete()
            self.message = await self.bot.guild.system_channel.send(embed=self.embed)
            self.embed = None

    async def cog_unload(self):
            self.timesignal.stop()
async def setup(bot):
    await bot.add_cog(Timesignal(bot))
