import disnake
from disnake.ext import commands

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="Botの応答速度を計測します")
    async def ping(self, interaction:  disnake.CommandInteraction):
        if round(self.bot.latency *1000) < 100:
            emoji = "<:stable_ping:1066023249751846942>"
        elif round(self.bot.latency *1000) < 200:
            emoji = "<:unstable_ping:1066023212284121189>"
        else:
            emoji = "<:interruption:1066023323898744912>"
        await interaction.response.send_message(embed=disnake.Embed(title=":ping_pong: Pong!", description=f"botの応答速度は、{emoji}{(self.bot.latency)*1000:.0f}msです。", color=disnake.Color.from_rgb(128,255,0)))
def setup(bot):
    bot.add_cog(Tools(bot))
