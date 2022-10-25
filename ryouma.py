import discord
import requests
import json
from discord.ext import commands

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='a.')
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')


@bot.command()
async def test(ctx):
    await ctx.send('めっせーじだよ')
@commands.group()
async def api(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('なにか指定して下さい')
@api.command()
async def title(ctx, url):
    url = requests.get("https://api.aic-group.net/get/title?p="+url+"&type=json")
    jsonText = url.text
    data = json.loads(jsonText)
    await ctx.reply("指定されたURLのtitleを取得しました。\n > タイトル:"+data["title"]+"\n > URL:"+url)

    
bot.run(ryoumatoken)



