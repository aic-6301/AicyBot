import discord
from discord.ext import commands


class Vc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        create_channel = self.bot.get_channel(1030990534984081538)
        unei_channel = self.bot.get_channel(1061523318458548244)
        if member.bot is False:
            if before.channel != after.channel:
                if after.channel == create_channel:
                    category = self.bot.get_channel(949560203886604291)
                    created_vc = await category.create_voice_channel(name=f"{member.name}の部屋")
                    await member.move_to(created_vc)
                    await created_vc.send(f"{member.mention}さんの部屋ができました。")


                if before.channel is not None:
                    if before.channel is create_channel or unei_channel:
                        return
                    if len(before.channel.members) == 0:
                        if len(before.channel.members) != 0:
                            for bot in before.channel.members:
                                bot.move_to(None)
                        await before.channel.delete()

async def setup(bot):
    await bot.add_cog(Vc(bot))
