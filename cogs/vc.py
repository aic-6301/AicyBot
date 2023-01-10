import discord
from discord.ext import commands


class settings(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        discord.ui.view.timeout = None # タイムアウトをなしに
        self.bot = bot.bot
    
    @discord.ui.button(label="ビッドレートの設定",style=discord.ButtonStyle.secondary, emoji='🔉', row=1)
    async def set_bit(self, interaction: discord.Integration, interaction_message: discord.InteractionMessage):
        member_id = interaction_message
        if interaction.user.id is member_id:
            await interaction.response.send_message('どれがいいか選択してね', view=select_bit, ephemeral=True)



class select_bit(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="8kbps"),
            discord.SelectOption(label="16kbps"),
            discord.SelectOption(label="32kbps"),
            discord.SelectOption(label="64kbps"),
            discord.SelectOption(label="128kbps")
        ]
    
        super().__init__(placeholder='', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0]:
            await interaction.channel.edit(bitrate=8)
        if self.values[1]:
            await interaction.channel.edit(bitrate=16)
        if self.values[2]:
            await interaction.channel.edit(bitrate=32)
        if self.values[3]:
            await interaction.channel.edit(bitrate=64)
        if interaction.guild.premium_subscription_count == 1:
            if self.values[4]:
                await interaction.channel.edit(bitrate=128)
        else:
            await interaction.response.send_message('変更できませんでした。', ephemeral=True)



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
                    embed = discord.Embed(title="設定")
                    await created_vc.send(f"{member.id}",embed=embed, view=settings(self))


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
