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
            e=discord.Embed(title='Apiのヘルプ', description='Apiを使ったコマンド集です')
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
                    await ctx.send('URLが存在しません。別のURLを試してみて下さい')
    
    @ping.command()
    async def websocket(self, ctx, url=None):
        await ctx.send(f'pong!:ping_pong: {round(self.bot.latency * 1000)}ms')
    
    @commands.command()
    async def status(self, ctx):
        if ctx.invoked_subcommand is None:
            try:
                e=discord.Embed(title='取得中・・・', description='少し待ってね', color=discord.Colour.from_rgb(160, 106, 84))
                msg = await ctx.send(embed=e)
                url = requests.get("https://api.aic-group.net/get/status")
                text = url.text
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
    async def color(self, ctx, color=None):
        msg = await ctx.send('取得中・・・')
        new_color = color.replace('#')
        msg.edit('https://api.aic-group.net/get/color.php?px=700&color='+new_color)
        

async def setup(bot):
    await bot.add_cog(info(bot))
