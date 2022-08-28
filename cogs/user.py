import discord
from discord.ext import commands
from datetime import timedelta, timezone


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ui", "user"])
    async def userinfo(self, ctx, user: discord.User = None):
        if user == None:
            user = ctx.author
        member = ctx.guild.get_member(user.id)
        if member is not None:
            user = member
        embed = discord.Embed(title=f'{user}の詳細', description=f'{user}の詳しい情報が載っています。', color=user.color)
        embed.add_field(name='名前', value=user)
        if user.bot == True:
            bot = 'はい'
        else:
            bot = 'いいえ'
        embed.add_field(name='Botかどうか', value=bot)
        embed.add_field(name='ID', value=user.id)
        embed.set_thumbnail(url=user.avatar)
        if member is not None:
            joined_at = member.joined_at.astimezone(timezone(timedelta(hours=9))).strftime(
                "%Y/%m/%d %H:%M:%S"
            )
            embed.add_field(name="サーバー参加日", value=joined_at, inline=False)
        created_at = user.created_at.astimezone(timezone(timedelta(hours=9))).strftime(
        "%Y/%m/%d %H:%M:%S"
        )
        embed.add_field(name="アカウント作成日", value=created_at, inline=False)
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(User(bot))
