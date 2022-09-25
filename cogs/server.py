import discord
from datetime import timezone, timedelta
from discord.ext import commands
from mcpi import minecraft
import os
import requests
import json
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
    @commands.group()
    async def mc(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('a!mc start でサーバーを実行できるはずだよ！！')
    @mc.command(name='start')
    async def start(self, ctx):
        if self.bot.guild == True:
            uri = requests.get("https://api.aic-group.net/get/status")
            text = uri.text
            data = json.loads(text)
            print(data)
            if (data['Minecraft Server']) == 'OK':
                await ctx.reply('サーバーはすでに起動済みです!')
            else:
                await ctx.send('サーバーの起動を開始します')
                os.system('systemctl start mc')
    @mc.command()
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        if self.bot.guild == True:
            uri = requests.get("https://api.aic-group.net/get/status")
            text = uri.text
            data = json.loads(text)
            if (data['Minecraft Server']) == 'OK':
                await ctx.reply('1分後にサーバーを停止します')
                mc.postToChat("1分後にサーバーを停止します")
                time.sleep(60)
                mc.postToChat("サーバーを停止します")
                os.system('systemctl stop mc')
            else:
                await ctx.reply('すでにサーバーは停止されています!')
    @mc.command()
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx):
        if self.bot.guild == True:
            uri = requests.get("https://api.aic-group.net/get/status")
            text = uri.text
            data = json.loads(text)
            if (data['Minecraft Server']) == 'OK':
                await ctx.reply('1分後にサーバーを再起動します')
                mc.postToChat("1分後にサーバーを再起動します")
                time.sleep(60)
                mc.postToChat("サーバーを再起動します")
                os.system('systemctl restart mc')
            else:
                await ctx.reply('サーバーは停止されています!')
    @commands.Cog.listener()
    async def on_message(self, ctx, message):
        #if message == discord.MessageType.premium_guild_subscription:
            member = message.author.id
            await member.add_roles(1015602734684184677)
            embed = discord.Embed(title='ブースト!!!', description='ブーストありがとうございます!!')
            embed.add_field(name='現在のブースト数', value=ctx.guild.premium_subscription_count+'個')
            embed.add_field(name='現在のサーバーレベル', value=ctx.guild.premium_tier+'レベル')
            if ctx.guild.premium_tier == 3:
                embed.add_field(name='サーバーレベル3達成!!', value='ブーストしてくれた人ありがとうございます！！')
            else:
                want_boost = (14-ctx.guild.premium_subscription_count)
                embed.add_field(name='サーバーレベル3まで', value=want_boost+'個です')
            await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Server(bot))
