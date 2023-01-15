import discord
from discord.ext import commands
from data import eew_data
import json
import requests

class Tool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="tools", with_app_command=True)
    async def tools(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.not_found(ctx)
    @tools.command(name="earthquake", with_app_command=True)
    async def earthquake(self, ctx):
        response = requests.get('https://dev.narikakun.net/webapi/earthquake/post_data.json')
        text = response.text()
        data = json.loads(text)
        await ctx.send(embed=await eew_data(data))
async def setup(bot):
    await bot.add_cog(Tool(bot))
