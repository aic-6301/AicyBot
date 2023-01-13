import discord
from discord.ext import commands
from discord import app_commands
import requests
import os
from typing import Literal
import googlesearch


class tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="tools", description="ツール類", guild_ids=None, guild_only=False)

    @group.command(name="search", description="いろいろなところで調べられます")
    async def search(self, interaction: discord.Interaction, text, site: Literal["google","YouTube","Pixiv"] = None):
        if site == "google":
            embed = discord.Embed(title="Google Search")
            for url in googlesearch.search(text, lang="jp", num=5):
                embed.add_field(name=f"{url['title']}")
                count += 1
                if(count == 5):
                    break
                await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(tools(bot))
