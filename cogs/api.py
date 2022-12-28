from typing import ValuesView
import discord
import discord.ui
from discord.ext import commands, tasks
from discord import app_commands
import requests
import json
import os
from pytube import extract
from typing import Optional, Literal
import asyncio

class button(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        discord.ui.view.timeout = None # タイムアウトをなしに
        self.bot = bot.bot
    
    @discord.ui.button(label="削除する",style=discord.ButtonStyle.danger, emoji='🗑️', row=1)
    async def delete_message(interaction: discord.Integration):
        await interaction.delete_original_message()

class dutton(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot.bot
    
    @discord.ui.button(label="削除する",style=discord.ButtonStyle.danger, emoji='🗑️', row=1, disabled=True)
    async def delete_message(interaction: discord.Integration):
        await interaction.delete_original_message()


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
                url = requests.get(f"https://api.aic-group.net/v1/tools/ping/")
                text = url.text
                data = json.loads(text)
                await ctx.send('ping値' + str(data['ping']) + f'\n' + 'ping先:' + (data['domain']))
            if url == 'websocket':
                embed=discord.Embed(title=':ping_pong:Pong!', description=f"{round(self.bot.latency * 1000)}ms")
                await ctx.send(embed=embed)
            else:
                try:
                    url = requests.get(f"https://api.aic-group.net/v1/tools/ping/?ip="+url+"&type=json")
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
                if (data['AicyWeb']['status']):
                    status = ':white_check_mark:[アクセス可能'
                    embed.add_field(name='AicyWeb', value=status+']('+ data['AicyWeb']['url'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='AicyWeb', value=status)
                if (data['AicyBlog']['status']):
                    status = ':white_check_mark:[アクセス可能'
                    embed.add_field(name='ブログサイト', value=status+']('+ data['AicyBlog']['url'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='ブログサイト', value=status)
                if (data['AicyWiki']['status']):
                    status = ':white_check_mark:[アクセス可能'
                    embed.add_field(name='AicyWiki', value=status+']('+ data['AicyWiki']['url'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='AicyWiki', value=status)
                if (data['AicyMedia']['status']):
                    status = ':white_check_mark:[アクセス可能'
                    embed.add_field(name='メディアサイト', value=status+']('+ data['AicyMedia']['url'][0] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='メディアサイト', value=status)
                if (data['AicyAPI']['status']):
                    status = ':white_check_mark:[アクセス可能'
                    embed.add_field(name='AicyAPI', value=status+']('+ data['AicyAPI']['url'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='API', value=status)
                if (data['Minecraft']['status']['Proxy']):
                    proxy_status = ':white_check_mark:プロキシ：アクセス可能'
                else:
                    proxy_status = ':octagonal_sign:アクセス不可'
                if (data['Minecraft']['status']['AicyCraft']):
                    main_status = ':white_check_mark:AicyCraft：アクセス可能'
                else:
                    main_status = ':octagonal_sign:アクセス不可'
                if (data['Minecraft']['status']['AicySurvival']):
                    sub_status = ':white_check_mark:AicySurvival：アクセス可能'
                else:
                    sub_status = ':octagonal_sign:アクセス不可'
                embed.add_field(name='マイクラサーバー', value=f'{proxy_status}\n{main_status}\n{sub_status}')
                if (data['AicyLive']['status']['status']):
                    status = ':white_check_mark:[アクセス可能'
                    if (data['AicyLive']['status']['stream']):
                        live_status = ':white_check_mark:配信中'
                    else:
                        live_status = ':octagonal_sign:配信されていません。'
                    embed.add_field(name='AicyLive', value=status+']('+ data['AicyLive']['url'] +f')\n{live_status}')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='AicyLive', value=status)
                await msg.edit(embed=embed)
    @api.command(description="色を取得")
    async def color(self, ctx, color):
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
        await ctx.send(f'https://api.aic-group.net/v1/color/{new_color}')
    @commands.hybrid_command(with_app_command=True, description="ニュースを取得")
    async def news(self, ctx):
        e = discord.Embed(title='<a:lllloading:1023933608983015524> 取得中', description='少し待ってね', color=discord.Colour.from_rgb(160, 106, 84))
        msg = await ctx.send(embed=e)
        try:
            url = requests.get(f'https://api.aic-group.net/v1/news/mainline/')
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
            url = requests.get(f'https://api.aic-group.net/v1/tools/shorturl/?url={url}')
            text = url.text
            data = json.loads(text)
        if id is not None:
            if self.bot.vip.members:
                url = requests.get(f'https://api.aic-group.net/v1/tools/shorturl/?url={url}&id={id}')
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
    @app_commands.describe(type='audio/videoのどちらかを選択。選択しなければ、audioが選択されます。')
    async def download(self, ctx, url, type: Literal['audio', 'video']=None):
        if type is None or type == 'audio':
            msg = await ctx.send(embed=discord.Embed(title='<a:lllloading:1023933608983015524>ダウンロード中・・', color=discord.Colour.from_rgb(160, 106, 84)))
            request = requests.get(f"https://api.aic-group.net/tools/dl?url={url}&type=audio")
            text =request.text
            data = json.loads(text)
            if "ファイルの生成に成功しました。\nこのファイルはまもなく削除される予定です。" in data['message']:
                e = discord.Embed(title='成功',description='このファイルは一時間以内に消されます。', color=discord.Colour.from_rgb(160, 106, 84))
                e.add_field(name='ダウンロードリンク', value=data['url']+' ('+data['size']+')')
                await msg.edit(embed=e)
            else:
                await msg.reply('失敗しました。後ほどお試しください。')
        if type == 'video':
            msg = await ctx.send(embed=discord.Embed(title='<a:lllloading:1023933608983015524>ダウンロード中・・', color=discord.Colour.from_rgb(160, 106, 84)))
            request = requests.get(f"https://api.aic-group.net/get/dl?url={url}&type=video")
            text =request.text
            data = json.loads(text)
            if "ファイルの生成に成功しました。\nこのファイルはまもなく削除される予定です。" in data['message']:
                e = discord.Embed(title='成功',description='<:warning:1053517470377463859>このファイルはまもなく削除されます。お早めにダウンロードをお願いします。', color=discord.Colour.from_rgb(160, 106, 84))
                e.add_field(name='ダウンロードリンク', value=data['url']+' ('+data['size']+')')
                await msg.edit(embed=e)
            else:
                await msg.edit('失敗しました。後ほどお試しください。')
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content in 'youtube.com/watch?v=' or 'youtu.be/watch?v=':
            try:
                id=extract.video_id(message.content)
            except:
                    id=None
            if id is None:
                return
            else:
                url=requests.get(f'https://api.aic-group.net/v1/tools/youtube/videoinfo/{id}')
                text = url.text
                data = json.loads(text)
                viewcount= "{:,}".format(data['info']['viewCount'])
                embed = discord.Embed(title=data['info']['title'], description=f"{data['info']['title']}の情報です", color=discord.Color.red(), url=message.content)
                if len(data['info']['description']) <= 500:
                    embed.add_field(name="概要欄", value=data['info']['description'])
                embed.add_field(name="アップロード日", value=f"<t:{data['info']['upload']}:f>(<t:{data['info']['upload']}:R)")
                embed.set_author(name=data['info']['channel']['name'], url=data['info']['channel']['url'])
                embed.set_image(url=data['meta']['thumb'])
                embed.set_footer(text=f"{viewcount}回視聴")
                msg = await message.channel.send(embed=embed, view=dutton(self))
                await asyncio.sleep(60)
                await msg.edit(embed=embed, view=dutton(self))



async def setup(bot):
    await bot.add_cog(api(bot))
