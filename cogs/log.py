import discord
from discord.ext import commands
from datetime import datetime


class log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_delete(self, message):
        embed = discord.Embed(title="メッセージ削除")
        embed.set_author(name=message.author)
        embed.add_field(name="メッセージ", value=message.content, inline=False)
        if message.attachments and message.attachments[0].proxy_url:
            embed.add_field(name="添付ファイル"
            , value=message.attachments[0].proxy_url)
        embed.add_field(name="メッセージ送信日", value=datetime.date(message.created_at), inline=False)
        embed.add_field(name="削除された日", value=datetime.timestamp(datetime.now()), inline=False)
        embed.set_footer(text=f"Aicy -"+ datetime.now().strftime('%Y/%m/%d %H:%M'))
        await self.bot.get_channel()
    @commands.Cog.listener()
    async def on_edit(self,before, after):
        embed = discord.Embed(title="メッセージ編集")
        embed.set_author(name=before.author)
        embed.add_field(name="編集前メッセージ", value=before.content, inline=False)
        if before.attachments:
            embed.add_field(name="ファイル", value=before.attachments.url, inline=False)
        embed.add_field(name="編集後メッセージ", value=after.content, inline=False)
        if before.attachments:
            embed.add_field(name="ファイル", value=after.attachments.url, inline=False)
        embed.add_field(name="メッセージ送信日", value=datetime.timestamp(before.created_at), inline=False)
        embed.add_field(name="編集された日", value=datetime.timestamp(after.edited_at), inline=False)
        embed.set_footer(text=f"Aicy -"+ datetime.now().strftime('%Y/%m/%d %H:%M'))
        

async def setup(bot):
    await bot.add_cog(log(bot))
