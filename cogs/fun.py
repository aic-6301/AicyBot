import discord
import random
import asyncio
from discord.ext import commands
import requests
import bs4



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
    @commands.command()
    async def google(self, ctx, keyword):
        response = requests.get('https://www.google.co.jp/search?hl=jp&gl=JP&num=10&q=' + keyword)
        url = 'https://www.google.co.jp/search?hl=jp&gl=JP&q=' + keyword
        # ステータスコードが200以外なら例外を発生させる
        response.raise_for_status()

        # 取得したHTMLをパースする
        bs = bs4.BeautifulSoup(response.text, "html.parser")

        # 検索結果のタイトルとリンクを取得
        element = bs.select('.r > a')

        title_list = []
        url_list = []

        for i in range(len(element)):
            # タイトルのテキスト部分のみ取得
            title = element[i].get_text()    
            # リンクのみを取得し、余分な部分を削除する
            url = element[i].get('href').replace('/url?q=','')

            title_list.append(title)
            url_list.append(url)

        # 出力
        for i in range(len(title_list)):
            embed= discord.Embed(title='Google検索結果', description='上位五件を表示しています。')
            embed.add_field(name=title_list[i], value=url_list[i], inline=False)
            embed.set_thumbnail(url='https://i0.wp.com/osunbook6.com/wp-content/uploads/2020/03/icons8-%E3%82%AB%E3%83%A9%E3%83%BC-480.png?resize=300%2C300&ssl=1')
async def setup(bot):
    await bot.add_cog(Fun(bot))
