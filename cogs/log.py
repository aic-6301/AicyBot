import discord
from discord.ext import commands
from datetime import datetime


class log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(title="メッセージ削除")
        embed.set_author(name=message.author)
        embed.add_field(name="メッセージ", value=message.content, inline=False)
        if message.attachments:
            embed.add_field(name="ファイル", value=message.attachments.url, inline=False)
        embed.add_field(name="メッセージ送信日", value=datetime.timestamp(message.created_at), inline=False)
        embed.add_field(name="削除された日", value=datetime.timestamp(datetime.now()), inline=False)
        embed.set_footer(text=f"Aicy -"+ datetime.now().strftime('%Y/%m/%d %H:%M'))
    @commands.Cog.listener()
    async def on_message_edit(self,before, after):
        embed = discord.Embed(title="メッセージ編集")
        embed.set_author(name=before.message.author)
        embed.add_field(name="編集前メッセージ", value=before.message.content, inline=False)
        if before.message.attachments:
            embed.add_field(name="ファイル", value=before.message.attachments.url, inline=False)
        embed.add_field(name="編集後メッセージ", value=after.message.content, inline=False)
        if before.message.attachments:
            embed.add_field(name="ファイル", value=after.message.attachments.url, inline=False)
        embed.add_field(name="メッセージ送信日", value=datetime.timestamp(before.message.created_at), inline=False)
        embed.add_field(name="編集された日", value=datetime.timestamp(after.message.edited_at), inline=False)
        embed.set_footer(text=f"Aicy -"+ datetime.now().strftime('%Y/%m/%d %H:%M'))

async def setup(bot):
    await bot.add_cog(log(bot))
