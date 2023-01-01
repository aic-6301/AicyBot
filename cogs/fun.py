import discord
from discord.ext import commands
from discord import app_commands
import requests
from typing import Literal


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="fun", description="楽しい機能達", guild_ids=[949560203374915605], guild_only=True)
    @group.command(name="5000choyen", description="5000兆円apiを使った機能")
    @app_commands.describe(top="上の文字", bottom="下の文字")
    async def gosentyou(self, interaction: discord.Interaction, top: str, bottom: str):
        url = requests.get(f'https://gsapi.cbrx.io/image?top={top}&bottom={bottom}')
        with open('data/5000choyen.png', 'wb') as f:
            f.write(url.content)
        await interaction.response.send_message(file=discord.File("data/5000choyen.png"))
async def setup(bot):
    await bot.add_cog(Fun(bot))
