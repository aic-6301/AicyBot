import discord
import random
import asyncio
from discord.ext import commands


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

async def setup(bot):
    await bot.add_cog(Fun(bot))
