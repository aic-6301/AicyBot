import discord
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def basic(self, ctx):
        await ctx.send('hello')

async def setup(bot):
    await bot.add_cog(Basic(bot))
