import discord
from discord.ext import commands


class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def afk(self, ctx):
        await ctx.send('実装中・・・')

async def setup(bot):
    await bot.add_cog(Afk(bot))
