from typing import ValuesView
import discord
from discord.ext import commands, tasks
from discord import app_commands
import requests
import json
import os
from typing import Literal

class api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message = None
        self.embed = None
    @commands.hybrid_group(with_app_command=True, description="APIのコマンド集")
    async def api(self, ctx):
        if ctx.invoked_subcommand is None:
            e=discord.Embed(title='Apiのヘルプ', description='Apiを使ったコマンド集です', color=discord.Colour.from_rgb(160, 106, 84))
            e.add_field(name='ping', value='サイトへのpingを実行しています。')
            e.add_field(name='status', value='サーバー情報を取得します。')
            e.add_field(name='api color', value='色のサンプルを表示できます')
            await ctx.send(embed=e)
    @commands.group()
    async def ping(self, ctx, url=None):
        if ctx.invoked_subcommand is None:
            if url is None:
                url = requests.get(f"https://api.aic-group.net/get/ping?type=json")
                text = url.text
                data = json.loads(text)
                await ctx.send('ping値' + str(data['ping']) + f'\n' + 'ping先:' + (data['domain']))
            if url == 'websocket':
                await ctx.send(f'pong!:ping_pong: {round(self.bot.latency * 1000)}ms')
            else:
                try:
                    url = requests.get(f"https://api.aic-group.net/get/ping?type=json&ip="+url)
                    text = url.text
                    data = json.loads(text)
                    await ctx.send('ping値' + str(data['ping']) + f'\n' + 'ping先:' + (data['domain']))
                except:
                    await ctx.send('urlが存在しません。別のurlを試してみて下さい')

    @commands.hybrid_command(with_app_command=True, description="サーバーステーサスを取得")
    async def status(self, ctx):
        if ctx.invoked_subcommand is None:
                e=discord.Embed(title='<a:lllloading:1023933608983015524> 取得中・・・', description='少し待ってね', color=discord.Colour.from_rgb(160, 106, 84))
                msg = await ctx.send(embed=e)
                uri = requests.get("https://api.aic-group.net/v1/server/status/")
                text = uri.text
                data = json.loads(text)
                embed = discord.Embed(title='ステータス', description='サーバーのステータス情報です', color=discord.Colour.from_rgb(160, 106, 84))
                if (data['AicyWeb']['status']) == 'true':
                    status = ':white_check_mark:[アクセス可能'
                    embed.add_field(name='AicyWeb', value=status+']('+ data['AicyWeb']['url'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='AicyWeb', value=status)
                if (data['AicyBlog']['status']) == 'true':
                    status = ':white_check_mark:[アクセス可能'
                    embed.add_field(name='ブログサイト', value=status+']('+ data['AicyBlog']['url'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='ブログサイト', value=status)
                if (data['AicyWiki']['status']) == 'true':
                    status = ':white_check_mark:[アクセス可能'
                    embed.add_field(name='AicyWiki', value=status+']('+ data['AicyWiki']['url'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='AicyWiki', value=status)
                if (data['AicyMedia']['status']) == 'true':
                    status = ':white_check_mark:[アクセス可能'
                    embed.add_field(name='メディアサイト', value=status+']('+ data['AicyMedia']['url'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='メディアサイト', value=status)
                if (data['AicyAPI']['status']) == 'true':
                    status = ':white_check_mark:[アクセス可能'
                    embed.add_field(name='AicyAPI', value=status+']('+ data['AicyAPI']['url'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='API', value=status)
                if (data['AicyGit']['status']) == 'true':
                    status = ':white_check_mark:[アクセス可能'
                    embed.add_field(name='AicyGit', value=status+']('+ data['AicyGit']['url'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='AicyGit', value=status)
                embed.add_field(name='マイクラサーバーステータス', value=status)
                if (data['Minecraft']['status']['Proxy']) == 'true':
                    proxy_status = ':white_check_mark:プロキシ：アクセス可能'
                else:
                    proxy_status = ':octagonal_sign:アクセス不可'
                if (data['Minecraft']['status']['AicyCraft']) == 'true':
                    main_status = ':white_check_mark:AicyCraft：アクセス可能'
                else:
                    main_status = ':octagonal_sign:アクセス不可'
                if (data['Minecraft']['status']['AicySurvival']) == 'true':
                    sub_status = ':white_check_mark:AicySurvival：アクセス可能'
                else:
                    sub_status = ':octagonal_sign:アクセス不可'
                embed.add_field(name='マイクラサーバー', value=f'{proxy_status}\n{main_status}\n{sub_status}')
                if (data['AicyLive']['status']['status']) == 'true':
                    status = ':white_check_mark:[アクセス可能'
                    if (data['AicyLive']['status']['stream']) == 'true':
                        live_status = ':white_check_mark:配信中'
                    else:
                        live_status = ':octagonal_sign:配信されていません。'
                    embed.add_field(name='AicyLive', value=status+']('+ data['AicyLive']['url'] +f')\n{live_status}')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='AicyLive', value=status)
                await msg.edit(embed=embed)
    @api.command(description="色を取得")
    async def color(self, ctx, color, size=None):
        try:
            size = size.replace('px', '')
        except:
            pass
        try:
            new_color = color.replace('#','')
        except:
            pass
        if size is None:
            new_size = 300
        else:
            new_size = size
        await ctx.send(f'https://api.aic-group.net/get/color.php?px={new_size}&color='+new_color)
    @commands.hybrid_command(with_app_command=True, description="ニュースを取得")
    async def news(self, ctx):
        e = discord.Embed(title='<a:lllloading:1023933608983015524> 取得中', description='少し待ってね', color=discord.Colour.from_rgb(160, 106, 84))
        msg = await ctx.send(embed=e)
        try:
            url = requests.get(f'https://api.aic-group.net/get/news.php?type=mainline')
            text = url.text
            data = json.loads(text)
            embed = discord.Embed(title='現在のニュースです', description='最新4件を表示しています', color=discord.Colour.from_rgb(160, 106, 84))
            embed.add_field(name=(data['main1']['title']), value='更新日:'+(data['main1']['date'])+f'\nURL:'+(data['main1']['uri']), inline=False)
            embed.add_field(name=(data['main2']['title']), value='更新日:'+(data['main2']['date'])+f'\nURL:'+(data['main2']['uri']), inline=False)
            embed.add_field(name=(data['main3']['title']), value='更新日:'+(data['main3']['date'])+f'\nURL:'+(data['main3']['uri']), inline=False)
            embed.add_field(name=(data['main4']['title']), value='更新日:'+(data['main4']['date'])+f'\nURL:'+(data['main4']['uri']), inline=False)
            await msg.edit(embed=embed)
        except:
            em = discord.Embed(title='ニュースを取得できませんでした', description='数秒後に実施してみてください。')
            await msg.edit(embed=em)
    @api.command(description="Nitroのコードを取得")
    async def nitro(self, ctx, count: int):
        response = requests.get(f"https://api.aic-group.net/get/nitro_gen.php?q={str(count)}")
        await ctx.send(response.text)
    @commands.hybrid_command(with_app_command=True, description="URLを短くします。")
    async def shorten(self, ctx, url, id=None):
        if id is None:
            url = requests.get(f'https://api.aic-group.net/get/shorten?url={url}')
            text = url.text
            data = json.loads(text)
        if id is not None:
            if self.bot.vip.members:
                url = requests.get(f'https://api.aic-group.net/get/shorten?url={url}&id={id}')
                text = url.text
                data = json.loads(text)
            else:
                await ctx.send('vipではないのでidを指定できません。')
        if url is None:
            await ctx.reply('URLを入力してください。')
        if data['type'] == 'URI Syntax Error':
            await ctx.send(data['messeage']+f'\nURLを直してお試しください。')
        else:
            e = discord.Embed(title='URL短縮', description='URLの短縮に成功しました', color=discord.Colour.from_rgb(160, 106, 84))
            e.add_field(name='リンク', value=(data['url']))
            await ctx.send(embed=e)
    @commands.hybrid_command(with_app_command=True, description="動画をダウンロード")
    @app_commands.describe(type='audio/videoのどちらかを選択。標準ではaudioが選択されてます')
    async def download(self, ctx, url, type: Literal['audio', 'video']=None):
        if type is None or type == 'audio':
            msg = await ctx.send(embed=discord.Embed(title='<a:lllloading:1023933608983015524>ダウンロード中・・', color=discord.Colour.from_rgb(160, 106, 84)))
            request = requests.get(f"https://api.aic-group.net/get/dl?url={url}&type=audio")
            text =request.text
            data = json.loads(text)
            if "ファイルの生成に成功しました。\nこのファイルはまもなく削除される予定です。" in data['message']:
                e = discord.Embed(title='成功',description='このファイルは一時間以内に消されます。', color=discord.Colour.from_rgb(160, 106, 84))
                e.add_field(name='ダウンロードリンク', value=data['url']+' ('+data['size']+')')
                await msg.edit(embed=e)
            else:
                await msg.reply('失敗しました。後ほどお試しください。')
        if type == 'video':
            msg = await ctx.send(embed=discord.Embed(title='ダウンロード中・・', color=discord.Colour.from_rgb(160, 106, 84)))
            request = requests.get(f"https://api.aic-group.net/get/dl?url={url}&type=video")
            text =request.text
            data = json.loads(text)
            if "ファイルの生成に成功しました。\nこのファイルはまもなく削除される予定です。" in data['message']:
                e = discord.Embed(title='成功',description='このファイルはまもなく削除されます。お早めにダウンロードをお願いします。', color=discord.Colour.from_rgb(160, 106, 84))
                e.add_field(name='ダウンロードリンク', value=data['url']+' ('+data['size']+')')
                await msg.edit(embed=e)
            else:
                await msg.edit('失敗しました。後ほどお試しください。')




async def setup(bot):
    await bot.add_cog(api(bot))
