import discord
from discord.ext import commands
from datetime import timedelta, datetime


class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        if member.guild == self.bot.guild:
            if member.bot is True:
                botrole = self.bot.guild.get_role(957605879857963058)
                await member.add_roles(botrole)
                embed = discord.Embed(title="新規Bot追加", colour=discord.Colour(0xb22222), description="新しいBotが追加されたよ", timestamp=datetime.now())
                embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
                await self.bot.guild.system_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        Member_role = self.bot.guild.get_role(957605646231019540)
        if Member_role not in before.roles and Member_role in after.roles:
            join_jst = after.joined_at + timedelta(hours = 9)
            embed = discord.Embed(title="新規参加", colour=discord.Colour.random(), description="新しいユーザーが認証を終えて参加しました！\n歓迎してあげてね", timestamp=datetime.now())
            embed.add_field(name='入った人へ', value='<#964090566210121738>で自己紹介をお願いします。')
            embed.set_author(name=after.display_name, icon_url=after.display_avatar.url)
            embed.add_field(name="サーバー参加日時", value=join_jst.strftime("%Y/%m/%d, %H:%M:%S"), inline=False)
            await self.bot.guild.system_channel.send(embed = embed)
async def setup(bot):
    await bot.add_cog(Join(bot))
