import discord
from discord.ext import commands
import requests
import json


class Botinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                    await ctx.send('URLが存在しません。別のURLを試してみて下さい')
    
    @ping.command()
    async def websocket(self, ctx, url=None):
        await ctx.send(f'pong!:ping_pong: {round(self.bot.latency * 1000)}ms')
    
    @commands.command()
    async def status(self, ctx):
        if ctx.invoked_subcommand is None:
            e=discord.Embed(title='取得中・・・', value='少し待ってね', color='A06A54')
            msg = await ctx.send(embed=e)
            url = requests.get("https://api.aic-group.net/get/status")
            text = url.text
            data = json.loads(text)
            embed = discord.Embed(title='ステーサス', description='サーバーのステーサス情報です', color='A06A54')
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
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Botinfo(bot))
