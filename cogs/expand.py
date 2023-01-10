import discord
from dispander import dispand, delete_dispand

import discord
from discord.ext import commands


class Expand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        await dispand(message)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await delete_dispand(self.bot, payload=payload)


async def setup(bot):
    await bot.add_cog(Expand(bot))