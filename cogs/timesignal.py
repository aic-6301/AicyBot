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

    @tasks.loop(minutes=1)
    async def timesignal(self):
        dt_now = datetime.now().hour
        if datetime.now().second == '00':
            if datetime.now().minute == '00':
                self.embed = discord.Embed(title='時報', colour=discord.Colour(0x4b78e6), description=f'{dt_now}時ちょうどをお知らせします', color=discord.Colour.from_rgb(160, 106, 84))
                self.embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/984807772950519890/1003650594399064094/spin.gif')
                if dt_now == '00':
                    self.embed.add_field(name='あけおめ！！', value=f'今日は{datetime.now().year}/{datetime.now().month}/{datetime.now().day}です')
                elif dt_now == '06':
                    self.embed.add_field(name='おはよう！！！',value='ニュースはa!newsで見れるよ')
                elif dt_now == '12':
                    self.embed.add_field(name='お昼だよ！！！', value='ご飯を食べよう!!!')
                elif dt_now == '15':
                    self.embed.add_field(name='お菓子の時間！！！', value='お菓子を食べよう!!')
                elif dt_now == '18':
                    self.embed.add_field(name='夜ごはん！！！', value='夜ご飯を食べよう!!!')
                elif dt_now == '23':
                    self.embed.add_field(name='夜だよ！！！', value='そろそろねよう！！！')
            elif datetime.now().minute == '30':
                self.embed = discord.Embed(title='時報', colour=discord.Colour(0x4b78e6), description=f'{dt_now}時30分をお知らせします', color=discord.Colour.from_rgb(160, 106, 84))
                self.embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/984807772950519890/1003650594399064094/spin.gif')
            if datetime.now().month == '03':
                if datetime.now().date == '05':
                    if dt_now == '06':
                        if datetime.now().minute == '53':
                            await self.bot.guild.system_channel.send('@everyone サーバー設立一周年！！！！！！！')


        if self.embed != None:
            if self.message != None:
                await self.message.delete()
            self.message = await self.bot.guild.system_channel.send(embed=self.embed)
            self.embed = None


    async def cog_unload(self):
            self.timesignal.stop()
    @tasks.loop(seconds=30)
    async def minecraft(self):
        dt_now = datetime.now().hour
        if datetime.now().second == '00':
            if datetime.now().minute == '59':
                if dt_now == '03':
                    self.bot.get_channel(1046309521900970024).send('【自動アナウンス】定期再起動一分前です。再起動の時間になったら、一度サーバーから切断されます。サーバー性能維持のためご協力お願いします。')
                elif dt_now == '15':
                    self.bot.get_channel(1046309521900970024).send('【自動アナウンス】定期再起動一分前です。再起動の時間になったら、一度サーバーから切断されます。サーバー性能維持のためご協力お願いします。')
            if dt_now == '00':
                self.bot.get_channel(1046309521900970024).send(f'【自動アナウンス】おはようございます。今日は、{datetime.now().year}/{datetime.now().month}/{datetime.now().day}です。')

async def setup(bot):
    await bot.add_cog(Timesignal(bot))
