import discord
import os
import traceback
from discord.ext import commands, tasks
import logging
import requests
from json import load
from dotenv import load_dotenv

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
        print("定義中")
        bot.vc1 = bot.get_channel(959712448338870272)
        bot.vc2 = bot.get_channel(972040097358831627)
        bot.vc3 = bot.get_channel(972089138151047168)
        bot.vc1_owner = None
        bot.vc2_owner = None
        bot.vc3_owner = None
        bot.vc1_dash = None
        bot.vc2_dash = None
        bot.vc3_dash = None
        bot.vc1_status = 'Normal'
        bot.vc2_status = 'Normal'
        bot.vc3_status = 'Normal'
        bot.guild = bot.get_guild(949560203374915605)
        bot.vip = bot.guild.get_role(1015602734684184677)
        bot.everyone = bot.guild.get_role(949560203374915605)
        bot.boot_log = bot.get_channel(1011708105161179136)
        await bot.tree.sync()
        bot.maintenansmode = False
        print("定義完了")
        if bot.maintenansmode == True:
            await bot.change_presence(activity = discord.Activity(name=f"メンテナンスモードです。全機能が停止しています。", type=discord.ActivityType.playing), status='dnd')
            pass
        else:
            for file in os.listdir('./cogs'): # cogの中身ロード
                if file.endswith('.py'):
                    try:
                        await bot.load_extension(f'cogs.{file[:-3]}')
                        print(f'Loaded cogs.{file[:-3]}')
                    except:
                        traceback.print_exc()
                    await bot.change_presence(activity = discord.Activity(name=f"メンバー数:{len(bot.users)}人", type=discord.ActivityType.playing), status='online')
            embed = discord.Embed(title='起動通知', description=f'{bot.user}でログインしました。', color=discord.Colour.from_rgb(160, 106, 84))
            embed.add_field(name='メンバー数', value=f'{len(bot.users)}人')
            await bot.boot_log.send(embed=embed)
        print(f"Login successful. {bot.user}({bot.user.id})")

    async def getMyLogger(name):
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('./log/project.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(levelname)-9s  %(asctime)s  [%(name)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger




bot = aicyserer()

@bot.command()
@commands.is_owner()
async def maintenansmode(ctx, mode):
    if mode == 'True' or 'true' or 'yes' or 'on':
        bot.maintenansmode = True
        await ctx.send('メンテナンスモードが有効化されました\n全機能を停止します。')
        for file in os.listdir('./cogs'):
                if file.endswith('.py'):
                    try:
                        await bot.unload_extension(f'cogs.{file[:-3]}')
                    except:
                        traceback.print_exc()
    if mode == 'False' or 'false' or 'no' or 'off':
        bot.maintenansmode = False
        await ctx.send('メンテナンスモードが無効化されました\n再起動をします')
        exit()

if __name__ == "__main__":
    print("プログラムを実行しています。")
    try:
        bot.run(token)
    except:
        traceback.print_exc()
    print("===========実行完了===========")
