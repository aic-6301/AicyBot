import discord
from discord.ext import commands
from datetime import datetime

def time():
    return datetime.now()

class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.is_timed_out() == True:
            await self.bot.guild.get_channel(1063711350695673897).send(embed=discord.Embed(title="タイムアウト",
            description=f"{after.mention}はタイムアウトが付与されました！\n解除予定時刻:{discord.utils.format_dt(after.timed_out_until)}({discord.utils.format_dt(after.timed_out_until, style='R')})"))
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        if guild is not self.bot.guild:
            return
        await self.bot.guild.get_channel(1063711350695673897).send(embed=discord.Embed(title="BAN",
            description=f"{member.mention}({member.id})がBANされました。"))
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.bot.guild.get_channel(1063711355225505872).send(embed=discord.Embed(title="メッセージ編集", description=f"編集前:{before.message.content}\n編集後:{after.message.content}, 編集日時:{after.message.edited_at}"))


async def setup(bot):
    await bot.add_cog(Log(bot))
