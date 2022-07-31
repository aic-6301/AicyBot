import discord
from discord.ext import commands, tasks
from datetime import datetime

class remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.removetime.start()
        

    @tasks.loop()
    async def removetime(self, message):
        channel = self.bot.get_channel(98820905553115960) # 削除するチャンネル取得
        log = self.bot.get_channel(996709722533146726) # logチャンネル取得
        dt_now = datetime.now()
        if int(dt_now.hour) == 0:
            message = channel.message # どうやってメッセージ取得するかわからん
            await message.delete(1000)
            embed = discord.embed(title='定期削除', description='1日経過したのでつぶやき部屋のメッセージを削除しました。')
            log.send(embed=embed) # ログチャンネルに送信


async def setup(bot):
    await bot.add_cog(remove(bot))
