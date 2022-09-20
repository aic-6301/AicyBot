from http.client import responses
import discord
from discord.ext import commands, tasks
import requests
import json
import os


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.livestatus.start()
        self.message = None
        self.embed = None
    @commands.group()
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
            else:
                try:
                    url = requests.get(f"https://api.aic-group.net/get/ping?type=json&ip="+url)
                    text = url.text
                    data = json.loads(text)
                    await ctx.send('ping値' + str(data['ping']) + f'\n' + 'ping先:' + (data['domain']))
                except:
                    await ctx.send('urlが存在しません。別のurlを試してみて下さい')
    
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
                    status = ':white_check_mark:アクセス可能'
                    embed.add_field(name='AicyWeb', value='['+status+']('+ data['MainSiteURI'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='AicyWeb', value=status)
                if (data['AicyBlog']) == 'OK':
                    status = ':white_check_mark:アクセス可能'
                    embed.add_field(name='ブログサイト', value='['+status+']('+ data['AicyBlogURI'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='ブログサイト', value=status)
                if (data['AicyWiki']) == 'OK':
                    status = ':white_check_mark:アクセス可能'
                    embed.add_field(name='AicyWiki', value='['+status+']('+ data['AicyWikiURI'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='AicyWiki', value=status)
                if (data['AicyMedia']) == 'OK':
                    status = ':white_check_mark:アクセス可能'
                    embed.add_field(name='メディアサイト', value='['+status+']('+ data['AicyMediaURI'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='メディアサイト', value=status)
                if (data['AicyAPI']) == 'OK':
                    status = ':white_check_mark:アクセス可能'
                    embed.add_field(name='AicyAPI', value='['+status+']('+ data['AicyAPIURI'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='API', value=status)
                if (data['AicyGit']) == 'OK':
                    status = ':white_check_mark:アクセス可能'
                    embed.add_field(name='AicyGit', value='['+status+']('+ data['AicyGitURI'] +')')
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='AicyGit', value=status)
                await msg.edit(embed=embed)
                if (data['Minecraft Server']) == 'OK':
                    status = ':white_check_mark:アクセス可能'
                    embed.add_field(name='マイクラサーバー', value=status)
                else:
                    status = ':octagonal_sign:アクセス不可'
                    embed.add_field(name='マイクラサーバー', value=status)
                await msg.edit(embed=embed)
                if (data['Live Status']) == 'OK':
                    status = ':white_check_mark:配信中'
                    embed.add_field(name='AicyWeb', value='['+status+']('+ data['AicyLiveURI'] +')')
                else:
                    status = ':octagonal_sign:配信されていません'
                    embed.add_field(name='配信状況', value=status)
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
        e = discord.Embed(title='取得中', description='少し待ってね', color=discord.Colour.from_rgb(160, 106, 84))
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
    @api.command()
    async def nitro(self, ctx, count: int):
        response = requests.get(f"https://api.aic-group.net/get/nitro_gen.php?q={str(count)}")
        await ctx.send(response.text)
    @tasks.loop(minutes=1)
    async def livestatus(self):
        uri = requests.get("https://api.aic-group.net/get/status")
        text = uri.text
        data = json.loads(text)
        if (data['Live Status']) == 'OK':
            self.embed = discord.Embed(title="ライブが始まりました！", description='ライブを見に行きましょう！！！\nhttps://live.aic-group.net')
        else:
            self.message = None
        if self.embed != None:
            if self.message != None:
                pass
            else:
                self.message = await self.bot.guild.system_channel.send(embed=self.embed)
                self.embed = None

async def setup(bot):
    await bot.add_cog(info(bot))
