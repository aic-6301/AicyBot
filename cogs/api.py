from http.client import responses
import discord
from discord.ext import commands
import requests
import json


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.group()
    async def api(self, ctx):
        if ctx.invoked_subcommand is None:
            e=discord.Embed(title='Apiのヘルプ', description='Apiを使ったコマンド集です', color=discord.Colour.from_rgb(160, 106, 84))
            e.add_field(name='ping', value='サイトへのpingを実行しています。')
            e.add_field(name='status', value='サーバー情報を取得します。')
            e.add_field(name='color', value='色のサンプルを表示できます')
            await ctx.send(embed=e)
    @api.group()
    async def ping(self, ctx, url=None):
        if ctx.invoked_subcommand is None:
            if url is None:
                url = requests.get(f"https://api.aic-group.net/get/ping?type=json")
                text = url.text
                data = json.loads(text)
                await ctx.send('ping値' + str(data['ping']) + f'\n' + 'ping先:' + (data['domain']))
            else:
                try:
                    url = requests.get(f"https://api.aic-group.net/get/ping?type=json&ip="+url)
                    text = url.text
                    data = json.loads(text)
                    await ctx.send('ping値' + str(data['ping']) + f'\n' + 'ping先:' + (data['domain']))
                except:
                    await ctx.send('uriが存在しません。別のurlを試してみて下さい')
    
    @ping.command()
    async def websocket(self, ctx):
        await ctx.send(f'pong!:ping_pong: {round(self.bot.latency * 1000)}ms')
    
    @commands.command()
    async def status(self, ctx):
        if ctx.invoked_subcommand is None:
            try:
                e=discord.Embed(title='取得中・・・', description='少し待ってね', color=discord.Colour.from_rgb(160, 106, 84))
                msg = await ctx.send(embed=e)
                uri = requests.get("https://api.aic-group.net/get/status")
                text = uri.text
                data = json.loads(text)
                embed = discord.Embed(title='ステーサス', description='サーバーのステーサス情報です', color=discord.Colour.from_rgb(160, 106, 84))
                if (data['MainSite']) == 'OK':
                    status = ':white_check_mark:Online'
                    embed.add_field(name='メインサイト', value=status)
                else:
                    status = ':octagonal_sign:Offline'
                    embed.add_field(name='メインサイト', value=status)
                if (data['AicyBlog']) == 'OK':
                    status = ':white_check_mark:Online'
                    embed.add_field(name='ブログサイト', value=status)
                else:
                    status = ':octagonal_sign:Offline'
                    embed.add_field(name='ブログサイト', value=status)
                if (data['AicyWiki']) == 'OK':
                    status = ':white_check_mark:Online'
                    embed.add_field(name='Wikiサイト', value=status)
                else:
                    status = ':octagonal_sign:Offline'
                    embed.add_field(name='Wikiサイト', value=status)
                if (data['AicyMedia']) == 'OK':
                    status = ':white_check_mark:Online'
                    embed.add_field(name='メディアサイト', value=status)
                else:
                    status = ':octagonal_sign:Offline'
                    embed.add_field(name='メディアサイト', value=status)
                if (data['AicyAPI']) == 'OK':
                    status = ':white_check_mark:Online'
                    embed.add_field(name='API', value=status)
                else:
                    status = ':octagonal_sign:Offline'
                    embed.add_field(name='API', value=status)
                await msg.edit(embed=embed)
            except:
                await ctx.send('サイトへのアクセスに失敗しました。数秒後に実行してください。')
    @api.command()
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
    @commands.command()
    async def news(self, ctx):
        e = discord.Embed(title='取得中', description='少し待ってね')
        msg = await ctx.send(embed=e)
        try:
            url = requests.get(f'https://api.aic-group.net/get/news.php?type=mainline')
            text = url.text
            data = json.loads(text)
            print(data)
            embed = discord.Embed(title='現在のニュースです', description='最新4件を表示しています')
            embed.add_field(name=(data['main1']['title']), url=(data['main1']['uri']), value='更新日:'+(data['main1']['date']))
            embed.add_field(name=(data['main2']['title']), url=(data['main2']['uri']), value='更新日:'+(data['main2']['date']))
            embed.add_field(name=(data['main3']['title']), url=(data['main3']['uri']), value='更新日:'+(data['main3']['date']))
            embed.add_field(name=(data['main4']['title']), url=(data['main4']['uri']), value='更新日:'+(data['main4']['date']))
            await msg.edit(embed=embed)
        except:
            em = discord.Embed(title='ニュースを取得できませんでした', description='数秒後に実施してみてください。')
            await msg.edit(embed=em)

async def setup(bot):
    await bot.add_cog(info(bot))
