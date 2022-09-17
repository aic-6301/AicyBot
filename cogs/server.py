import discord
from datetime import timezone, timedelta
from discord.ext import commands
from mcpi import minecraft
import os
import time

mc = minecraft.Minecraft.create("mc.aic-group.net", 25565)

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["si"], description='実行した鯖のみ対応')
    async def serverinfo(self, ctx, guild:int=None):
        if guild == None:
            guild = ctx.guild
        roles = [role for role in guild.roles]
        text_channels = [text_channels for text_channels in guild.text_channels]
        embed = discord.Embed(title=f'サーバー情報 - {guild.name}', timestamp=ctx.message.created_at, color=discord.Colour.from_rgb(160, 106, 84))
        embed.add_field(name='サーバー名', value=f'{guild.name}',inline=False)
        embed.add_field(name='チャンネル数', value=f'{len(text_channels)}', inline=False)
        embed.add_field(name='ロール数', value=f'{len(roles)}', inline=False)
        embed.add_field(name='サーバーブースト数', value=guild.premium_subscription_count, inline=False)
        embed.add_field(name='メンバー数', value=f'{guild.member_count}', inline=False)
        embed.add_field(name='サーバー作成日', value=guild.created_at.strftime("%Y/%m/%d %H:%M:%S"), inline=False)
        embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)
    @commands.command()
    async def start(self, ctx):
        if self.bot.guild == True:
            if os.system('systemctl is-active mc') == 'active':
                await ctx.reply('サーバーはすでに起動済みです!')
            else :
                await ctx.send('サーバーの起動を開始します')
                os.system('systemctl start mc')
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        if self.bot.guild == True:
            if os.system('systemctl is-active mc') == 'active':
                await ctx.reply('1分後にサーバーを停止します')
                mc.postToChat("1分後にサーバーを停止します")
                time.sleep(60)
                mc.postToChat("サーバーを停止します")
                os.system('systemctl stop mc')
            else :
                await ctx.reply('すでにサーバーは停止されています!')
            

async def setup(bot):
    await bot.add_cog(Server(bot))
