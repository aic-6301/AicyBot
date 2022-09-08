import discord
import traceback
import os
import sys
import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv
import textwrap
from typing import List

load_dotenv()
token = os.environ.get('token')
bot = commands.Bot(command_prefix="a!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    bot.guild = bot.get_guild(949560203374915605)
    bot.admin = bot.guild.get_role(1002599926670295152)
    bot.guildadmin = bot.guild.get_role(957605810173796352)
    bot.log_ch = bot.get_channel(1004387301293555803)
    kidou = bot.get_channel(1011708105161179136)
    try:
        for file in os.listdir('./cogs'): # cogの中身ロード
            if file.endswith('.py'):
                await bot.load_extension(f'cogs.{file[:-3]}')
                print(f'{file[:-3]}を読み込んだよ!!')
    except:
        traceback.print_exc()
    try:
        await bot.load_extension('jishaku') # jishakuの読み込み
        print('jishakuを読み込んだよ!!')
    except:
        traceback.print_exc()
    try:
        await bot.load_extension("didyoumean_discordpy")
        print('didyoumean-discordpyを読み込んだよ!!')
    except:
        traceback.print_exc()
    print(f"Logged in as {bot.user}")
    guilds=len(bot.guilds)
    servers=str(guilds)
    embed = discord.Embed(title='起動通知', description=f'{bot.user}でログインしました。', color=discord.Colour.from_rgb(160, 106, 84))
    embed.add_field(name='導入サーバー数', value=f'{servers}鯖')
    embed.add_field(name='メンバー数', value=f'{len(bot.users)}人')
    await kidou.send(embed=embed)
    await bot.change_presence(activity = discord.Activity(name=f"メンバー数:{len(bot.users)}人, サーバー数:{len(bot.guilds)}サーバー", type=discord.ActivityType.playing), status='online')


@tasks.loop(seconds=30)
async def BotDD():
    requests.post("https://botdd.alpaca131.com/api/heartbeat",
                    headers={"Authorization": "7f72be94f652a089"})


@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am a robot")

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f':outbox_tray:`cogs.{extension}`')
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f':repeat:`cogs.{extension}`')

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f':inbox_tray:`cogs.{extension}`')

@bot.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.send('再起動します。。')
    exit()
@bot.event
async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("a")
bot.run(token)
