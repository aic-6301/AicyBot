import discord
import traceback
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get('token')
bot = commands.Bot(command_prefix="a!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    bot.guild = bot.get_guild(984807772333932594)
    bot.admin = bot.guild.get_role(1002599926670295152)
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')
            print(f'{file[:-3]}を読み込んだよ!!')
    try:
        await bot.load_extension('jishaku')
        print('jishakuを読み込んだよ!!')
    except:
        traceback.print_exc()
    print(f"Logged in as {bot.user}")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am a robot")

@bot.command()
async def reload(ctx, extension):
    admin = bot.admin
    if admin:
        await bot.reload_extension(f'cogs.{extension}')
        embed = discord.Embed(title='Reload!', description=f'{extension} Reloaded!', color=0xff00c8)
        await ctx.send(embed=embed)
    else:
        await ctx.send('このコマンドはbot管理者だけやで')



bot.run(token)
