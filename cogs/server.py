import discord
from datetime import timezone, timedelta
from discord.ext import commands


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["si"])
    async def serverinfo(self, ctx, guild: int =None):
        if guild == None:
            guild = ctx.guild
        roles = [role for role in guild.roles]
        text_channels = [text_channels for text_channels in guild.text_channels]
        embed = discord.Embed(title=f'サーバー情報 - {guild.name}', timestamp=ctx.message.created_at)
        embed.add_field(name='サーバー名', value=f'{guild.name}',inline=False)
        embed.add_field(name='チャンネル数', value=f'{len(text_channels)}', inline=False)
        embed.add_field(name='ロール数', value=f'{len(roles)}', inline=False)
        embed.add_field(name='サーバーブースト数', value=guild.premium_subscription_count, inline=False)
        embed.add_field(name='メンバー数', value=f'{guild.member_count}', inline=False)
        embed.add_field(name='サーバー作成日', value={guild.created_at.strftime(f'%Y/%m/%d %H:%M:%S')}, inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Server(bot))
