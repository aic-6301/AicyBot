import discord
from datetime import datetime
from discord.ext import commands


class Autoreply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='on_message')
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content == 'おはよう':
            if datetime.now().strftime('%H:%M') >= '12:00':
                await message.channel.send('もう昼だぞ')
            elif datetime.now().strftime('%H:%M') >= '18:00':
                await message.channel.send('もう夜だぞ')
            else:
                await message.channel.send('おはよう')
        if message.content == 'おやすみ':
            if datetime.now().strftime('%H:%M') <= '12:00':
                await message.channel.send('まだ朝だぞ')
            elif datetime.now().strftime('%H:%M') <= '18:00':
                await message.channel.send('まだ昼だぞ')
            else:
                await message.channel.send('おやすみ')
        if message.content == 'いってきます':
            await message.channel.send('いってらっしゃい！')
        if message.content == 'ただいま':
            await message.channel.send('おかえりなさい！')
        channel = self.bot.get_channel(1033496649395347456)
        msg = await channel.send(f"{message.author.name} - {message.content}")
        try:
            await msg.reply(f"{message.attachments.proxy_url[0]}")
        except:
            pass
async def setup(bot):
    await bot.add_cog(Autoreply(bot))
