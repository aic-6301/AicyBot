import discord
from discord.ext import commands


class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot == True:
            bot_role = self.bot.guild.get_role(1063686877829414964)
            await member.add_roles(bot_role)
            await self.bot.guild.system_channel.send(embed=discord.Embed(title="新規bot追加", description=f"新しいbotが来たよ\nBotの作成日時:{discord.utils.format_dt(member.created_at)}", color=discord.Color.red()).set_author(name=member.name, icon_url=member.avatar.url))
        if member is self.bot.get_user(784516723767640155):
            await member.add_roles(self.bot.guild.get_role(1067568142047526963))
        else:
            notfy_ch = self.bot.get_channel(1063711364360716350)
            await notfy_ch.send(embed=discord.Embed(title="新規ユーザー入室", description=f"{member.name}さん！いらっしゃいませ！あなたは{len(self.bot.guild.members)}人目のメンバーです！",color=discord.Color.green()))
            log_ch = self.bot.get_channel(1063711355225505872)
            await log_ch.send(embed=discord.Embed(title="ユーザー情報取得中・・"))
            embed = discord.Embed(title=f"{member.name}の情報", color=discord.Color.green())
            embed.add_field(name="ユーザーID", value=member.id, inline=False)
            embed.add_field(name="アカウント作成日時", value=member.created_at, inline=False)
            await log_ch.send(embed=embed)
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        Member_role = self.bot.guild.get_role(1063686877137350666)
        if Member_role not in before.roles and Member_role in after.roles:
            if after.bot:
                return
            await self.bot.guild.system_channel.send(embed=discord.Embed(title="新規ユーザー入室", description="新しいユーザーが認証を終わらせて入ってきたよ！\n歓迎してあげてね！！").set_author(name=after.name, icon_url=after.avatar.url))

async def setup(bot):
    await bot.add_cog(Join(bot))
