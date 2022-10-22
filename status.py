from sqlite3 import TimeFromTicks
import discord
from discord.ext import tasks, commands
from datetime import datetime
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
bot = commands.Bot(command_prefix='as!', intents=discord.Intents.all())
token = os.getenv('status_token')
@bot.event
async def on_ready():
    print(f'Logged in {bot.user}')
    status.start()
    await bot.load_extension("jishaku")

@tasks.loop(minutes=3)
async def status():
    await bot.change_presence(activity = discord.Activity(name=f"Server Running! 最終更新：{datetime.now().strftime('%H:%M')}", type=discord.ActivityType.streaming), status='idle')
    try:
        uri = requests.get("https://api.aic-group.net/get/status")
        text = uri.text
        data = json.loads(text)
    except:
        pass
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
    
    msg = await bot.get_channel(1030355963586289774).fetch_message(1033323482504777768)
    await msg.edit(embed=e)




bot.run(token)