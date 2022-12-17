import discord
from discord.ext import commands

async def get_id(id):
    await GetUser.get_user(id)

class GetUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_user(self, id):
        user = await self.bot.guild.get_member(id)
        

def setup(bot):
    bot.add_cog(GetUser(bot))
