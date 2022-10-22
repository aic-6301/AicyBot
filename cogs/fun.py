import discord
import random
import asyncio
from discord.ext import commands
import requests
import bs4
import json



class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx, choice):
        choices=["パー", "グー", "チョキ"]
        comp_choice = random.choice(choices)
        if choice == "パー":
            if comp_choice == "パー":
                await ctx.send(f"{comp_choice} 引き分け🙄")
            if comp_choice == "チョキ":
                await ctx.send(f"{comp_choice} あなたの負け")
            if comp_choice == "グー":
                await ctx.send(f"{comp_choice} あなたの勝ち👏")
        if choice == "チョキ":
            if comp_choice == "パー":
                await ctx.send(f"{comp_choice} あなたの勝ち👏")
            if comp_choice == "チョキ":
                await ctx.send(f"{comp_choice} 引き分け🙄")
            if comp_choice == "グー":
                await ctx.send(f"{comp_choice} あなたの負け")
        if choice == "グー":
            if comp_choice == "パー":
                await ctx.send(f"{comp_choice} あなたの負け")
            if comp_choice == "チョキ":
                await ctx.send(f"{comp_choice} あなたの勝ち👏")
            if comp_choice == "グー":
                await ctx.send(f"{comp_choice} 引き分け🙄")
        if choice not in choices:
            await ctx.send("じゃんけんにならないよ！！グーかチョキかパーを選んでね！！")
    @commands.hybrid_command(with_app_command=True, description='Powered by Google Trends')
    async def googletrend(self, ctx):
        response = requests.get('https://api.aic-group.net/get/trends')
        text = response.text
        data = json.loads(text)
        if data['channel']['item'][0]['description'] == '{}':
            description0 = 'なし'
        if data['channel']['item'][1]['description'] == '{}':
            description1 = 'なし'
        if data['channel']['item'][2]['description'] == '{}':
            description2 = 'なし'
        if data['channel']['item'][3]['description'] == '{}':
            description3 = 'なし'
        if data['channel']['item'][4]['description'] == '{}':
            description4 = 'なし'
        embed= discord.Embed(title='現在のトレンド', description='Google trendsから取得しています。')
        embed.add_field(name=data['channel']['item'][0]['title'], value=f"説明：{description0}\n{data['channel']['item'][0]['link']}")
        embed.add_field(name=data['channel']['item'][1]['title'], value=f"説明：{description1}\n{data['channel']['item'][1]['link']}")
        embed.add_field(name=data['channel']['item'][2]['title'], value=f"説明：{description2}\n{data['channel']['item'][2]['link']}")
        embed.add_field(name=data['channel']['item'][3]['title'], value=f"説明：{description3}\n{data['channel']['item'][3]['link']}")
        embed.add_field(name=data['channel']['item'][4]['title'], value=f"説明：{description4}\n{data['channel']['item'][4]['link']}")
        embed.set_footer(text='Powered by Google Trends')
        await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Fun(bot))
