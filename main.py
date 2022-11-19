import discord
import os
import traceback
from discord.ext import commands, tasks
import logging
import requests
from data.data import is_admin
from json import load
from dotenv import load_dotenv
import subprocess
from datetime import datetime
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
            with open('config.json', 'r+', encoding='utf-8') as file:
                bot.config = load(file)
            print('Config loaded')
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
        bot.admin_guild = bot.get_guild(1033496363897475163)
        bot.vip = bot.guild.get_role(1015602734684184677)
        bot.everyone = bot.guild.get_role(949560203374915605)
        bot.boot_log = bot.get_channel(1011708105161179136)
        await bot.tree.sync()
        bot.maintenansmode = False
        print("定義完了")
        if bot.maintenansmode == True:
            await bot.change_presence(activity = discord.Activity(name=f"メンテナンスモードです。全機能が停止しています。", type=discord.ActivityType.playing), status='dnd')
        else:
            for file in os.listdir('./cogs'): # cogの中身ロード
                if file.endswith('.py'):
                    try:
                        await bot.load_extension(f'cogs.{file[:-3]}')
                        print(f'Loaded cogs.{file[:-3]}')
                    except:
                        traceback.print_exc()
            await bot.tree.sync()
            embed = discord.Embed(title='起動通知', description=f'{bot.user}でログインしました。', color=discord.Colour.from_rgb(160, 106, 84))
            embed.add_field(name='メンバー数', value=f'{len(bot.users)}人')
            await bot.boot_log.send(embed=embed)
        print(f"Login successful. {bot.user}({bot.user.id})")
        status.start()

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

@bot.command()
async def restart(ctx):
    if ctx.author.roles:
        await ctx.reply('再起動します。', mention_author=False)
        exit()
    else:
        await ctx.reply('このコマンドは管理者専用です。')


@tasks.loop(minutes=3)
async def status():
        await bot.change_presence(activity = discord.Activity(name=f"Server Running! 最終更新：{datetime.now().strftime('%H:%M')} | メンバー数:{len(bot.users)}", type=discord.ActivityType.streaming), status='idle')
        try:
            uri = requests.get("https://api.aic-group.net/get/status")
            text = uri.text
            data = json.loads(text)
            status_message = None
            try:
                status_message.delete()
            except:
                pass
        except:
            if status_message != None:
                status_message = await bot.guild.system_channel.send('サーバーから応答がありません。\nOSフリーズまたはip変更の時間の可能性があります。')
        e = discord.Embed(title="各ステータス", color=discord.Colour.from_rgb(160, 106, 84), timestamp=datetime.now())
        e.clear_fields
        if (data['MainSite']) == 'OK':
            e.add_field(name="メインサイト", value='✅オンライン\n[サイトに行く](https://www.aic-group.net)')
        else:
            e.add_field(name="メインサイト", value='❌オフライン')
        if (data['AicyBlog']) == 'OK':
            e.add_field(name="ブログ", value='✅オンライン\n[サイトに行く](https://blog.aic-group.net)')
        else:
            e.add_field(name="ブログ", value='❌オフライン')
        if (data['AicyWiki']) == 'OK':
            e.add_field(name="Wiki", value='✅オンライン\n[サイトに行く](https://wiki.aic-group.net)')
        else:
            e.add_field(name="Wiki", value='❌オフライン')
        if (data['AicyAPI']) == 'OK':
            e.add_field(name="API", value='✅オンライン')
        else:
            e.add_field(name="API", value='❌オフライン')
        if (data['AicyMedia']) == 'OK':
            e.add_field(name="Media", value='✅オンライン\n[サイトに行く](https://media.aic-group.net)')
        else:
            e.add_field(name="Media", value='❌オフライン')
        if (data['AicyLive']) == 'OK':
            e.add_field(name="Live", value='✅オンライン\n[サイトに行く](https://live.aic-group.net)')
        else:
            e.add_field(name="Live", value='❌オフライン')
        if (data['AicyGit']) == 'OK':
            e.add_field(name="Git", value='✅オンライン\n[サイトに行く](https://git.aic-group.net)')
        else:
            e.add_field(name="Git", value='❌オフライン')
        if (data['Minecraft Server']) == 'OK':
            e.add_field(name="Minecraft", value='✅オンライン')
        else:
            e.add_field(name="Minecraft", value='❌オフライン')
        
        msg = await bot.get_channel(1030355963586289774).fetch_message(1043503405513060443)
        await msg.edit(embed=e)

if __name__ == "__main__":
    print("プログラムを実行しています。")
    try:
        bot.run(token)
    except:
        traceback.print_exc()
    print("===========実行完了===========")
