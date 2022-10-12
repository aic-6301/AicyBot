import discord
from datetime import timezone, timedelta
from discord.ext import commands
import os
import requests
import json
import time


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
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is None:
            if self.bot.guild:
                    if message == discord.MessageType.premium_guild_subscription:
                        member = message.author.id
                        await member.add_roles(1015602734684184677)
                        embed = discord.Embed(title='ブースト!!!', description='ブーストありがとうございます!!')
                        embed.add_field(name='現在のブースト数', value=message.guild.premium_subscription_count+'個')
                        embed.add_field(name='現在のサーバーレベル', value=message.guild.premium_tier+'レベル')
                        if message.guild.premium_tier == 3:
                            embed.add_field(name='サーバーレベル3達成!!', value='ブーストしてくれた人ありがとうございます！！')
                        else:
                            want_boost = (14-message.guild.premium_subscription_count)
                            embed.add_field(name='サーバーレベル3まで', value=want_boost+'個です')
                        await message.channel.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Server(bot))
