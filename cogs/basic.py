'''test用のコマンド'''
import discord
from discord import app_commands
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def basic(self, ctx):
        await ctx.send('hello')
    @app_commands.command()
    @app_commands.guilds(949560203374915605)
    @app_commands.guild_only()
    async def test(self, interaction):
        await interaction.response.send_message('やっほー！')

async def setup(bot):
    await bot.add_cog(Basic(bot))
