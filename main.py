import discord
import os
import traceback
from discord.ext import commands, tasks
from discord import app_commands
import logging
import requests
from json import load
from dotenv import load_dotenv
import subprocess
from datetime import datetime
import asyncio
import json

load_dotenv()
token = os.environ['token']

class aicyserer(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='a!',
            allowed_mentions=discord.AllowedMentions(replied_user=False),
            intents = discord.Intents.all()
            )
    async def on_ready(self):
        print(f"{bot.user}でログイン中・・・")
        await bot.change_presence(activity = discord.Activity(name=f"起動中・・・", type=discord.ActivityType.playing), status='dnd')
        try:
            await bot.load_extension("jishaku")
            print("Loaded jishaku")
        except:
            traceback.print_exc()
        try:
            await bot.load_extension("dispander")
            print("Loaded jishaku")
        except:
            traceback.print_exc()
        print("定義中")
        bot.guild = bot.get_guild(949560203374915605)
        bot.admin_guild = bot.get_guild(1033496363897475163)
        bot.vip = bot.guild.get_role(1015602734684184677)
        bot.everyone = bot.guild.get_role(949560203374915605)
        bot.boot_log = bot.get_channel(1058005805426814976)
        bot.owner = bot.get_user(964887498436276305)
        print("定義完了")
        for file in os.listdir('./cogs'): # cogの中身ロード
            if file.endswith('.py'):
                try:
                    await bot.load_extension(f'cogs.{file[:-3]}')
                    print(f'Loaded cogs: {file[:-3]}')
                except:
                    traceback.print_exc()
        await bot.tree.sync()
        embed = discord.Embed(title='起動通知', description=f'{bot.user}でログインしました。', color=discord.Colour.from_rgb(160, 106, 84))
        embed.add_field(name='メンバー数', value=f'{len(bot.users)}人')
        await bot.boot_log.send(embed=embed)
        print(f"Login successful. {bot.user}({bot.user.id})")
        while True:
            await bot.change_presence(activity = discord.Activity(name=f"Server Running! 最終更新：{datetime.now().strftime('%H:%M')} | メンバー数:{len(bot.users)}", type=discord.ActivityType.streaming), status='idle')
            await asyncio.sleep(30)

    async def not_found(self, ctx):
        await ctx.send(f"{ctx.command.name}のサブコマンドがないよ！`a!help {ctx.command.name}`をみてね！")
bot = aicyserer()




if __name__ == "__main__":
    print("プログラムを実行しています。")
    try:
        asyncio.sleep(3)
        bot.run(token)
    except:
        traceback.print_exc()
    print("===========実行完了===========")
