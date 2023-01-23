import disnake
from disnake.ext import commands


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        if isinstance(error, commands.errors.CommandNotFound):
            embed = disnake.Embed(
            title="❌コマンドが存在しません。",
            description="helpを参照してください",
            color=disnake.Color.red(),
        )
        else:
            embed = disnake.Embed(
                title="❌コマンド内でエラーが発生しました",
                description=f"```py\n{(error)}```",
                color=disnake.Color.red(),
            )
        await ctx.send(embed=embed)
    @commands.Cog.listener()
    async def on_slash_command_error(self, inter:disnake.AppCmdInter, error:commands.CommandError):
        embed = disnake.Embed(
            title="❌コマンド内でエラーが発生しました",
            description=(error),
            color=disnake.Color.red(),
        )
        if inter.response.is_done():
            send = inter.channel.send
        else:
            send = inter.response.send_message
        await send(embed=embed)

def setup(bot):
    bot.add_cog(Cog(bot))
