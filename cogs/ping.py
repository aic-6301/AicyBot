import discord
from discord.ext import commands
from ping3 import ping


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="ping", with_app_command=True)
    async def ping(self, ctx):
        await ctx.send(embed=discord.Embed(title=':ping_pong:Pong!', description=f'{round(self.bot.latency * 1000)}ms'))
    @ping.command(name="site", with_app_command=True)
    async def _site(self, ctx, target):
        result = int(ping(target, unit="ms"))
        await ctx.send(embed = discord.Embed(title=":ping_pong:Pong!",description=str(result) + "ms", color=discord.Colour.from_rgb(128,255,0)))
async def setup(bot):
    await bot.add_cog(Ping(bot))
