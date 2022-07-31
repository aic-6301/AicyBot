import discord
from discord.ext import commands


class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def news(self, ctx):
        # 誰か手伝って()
        await ctx.send('実装中だよ. もう少し待ってね')

async def setup(bot):
    await bot.add_cog(News(bot))
