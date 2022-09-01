import discord
import traceback
import os
import sys
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get('token')
bot = commands.Bot(command_prefix="a!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    bot.guild = bot.get_guild(949560203374915605)
    bot.admin = bot.guild.get_role(1002599926670295152)
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
    print(f"Logged in as {bot.user}")
    guilds=len(bot.guilds)
    servers=str(guilds)
    embed = discord.Embed(title='起動通知', description=f'{bot.user}でログインしました。', color=discord.Colour.from_rgb(160, 106, 84))
    embed.add_field(name='導入サーバー数', value=f'{servers}鯖')
    # embed.add_field(name='メンバー数', description=f'bot.usersmembers')
    await kidou.send(embed=embed)
    '''for guild in bot.guilds:
        print(len(guild.members))
        await bot.change_presence(activity = discord.Activity(name=f"メンバー数:{}, サーバー数:{servers}", type=discord.ActivityType.playing), status='online')'''

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

bot.run(token)
