import discord
from discord.ext import commands


class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 1033496649395347456:
            if message.author.bot:
                return
            await self.bot.get_channel(949560203886604293).send(message.author+' - '+message.content)
            await message.add_reaction('✅')
async def setup(bot):
    await bot.add_cog(Global(bot))
