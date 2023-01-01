import discord
from discord.ext import commands


class rename(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="チャンネル名変更",
            timeout=60,
        )
        self.value = None

        self.name = discord.ui.TextInput(
            label="新しいチャンネル名(空白でリセット)",
            style=discord.TextStyle.short,
            placeholder="VC-xx",
            required=False,
        )
        self.add_item(self.name)

    async def on_submit(self, interaction) -> None:
        self.value = self.name.value
        self.stop()
        if self.value != '':
            await interaction.response.send_message(f'チャンネル名を`{self.value}`に設定しました', ephemeral=True)
        else:
            await interaction.response.send_message('チャンネル名をリセットしました', ephemeral=True)



class Vc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        create_channel = self.bot.get_channel(1030990534984081538)
        if member.bot is False:
            if before.channel != after.channel:
                if after.channel == create_channel:
                    category = self.bot.get_channel(949560203886604291)
                    created_vc = await category.create_voice_channel(name=f"{member.name}の部屋")
                    await member.move_to(created_vc)
                    await created_vc.send(f"{member.mention}さんの部屋ができました。")


                if before.channel is not None:
                    if before.channel is create_channel:
                        return
                    if len(before.channel.members) == 0:
                        if len(before.channel.members) != 0:
                            for bot in before.channel.members:
                                bot.move_to(None)
                        await before.channel.delete()

async def setup(bot):
    await bot.add_cog(Vc(bot))
