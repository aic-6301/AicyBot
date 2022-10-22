import discord
from discord.ext import commands
from discord import ui
import random
from datetime import datetime




class owner():
    def __init__(self, bot):
        super().__init__()
        self.vcowner = None
    
    async def setup(self, member, after):
        if len(after.channel.members) == 1:
            if after.channel == discord.VoiceChannel:
                after.channel.owner = member
                embed = discord.Embed(title='VC用ダッシュボード', description='VCについて操作することができます。')
                embed.add_field(name='現在のVCオーナー :',value=self.bot.vc1_owner.mention)
                embed.set_footer(text='"</vctool dashboard:973928793154662410>"でダッシュボードを再送信できます')
                after.channel.dashboard = await self.bot.vc1.send(f'{member.mention}は{after.channel}の所有権を持っています', delete_after=60)
                await after.channel.send(embed=embed, view=dashboard(self))
    async def check(self, member, channel):
        if channel == channel and member == channel.owner:
            result = channel
    async def change(self, after):
        member = after.channel.members
        count = 0
        for user in member:
            if user.bot == True:
                member.pop(count)
            count + 1
        await after.channel.dashboard.delete()
        embed = discord.Embed(title="ダッシュボード", colour=discord.Colour(0x1122a6), description="VCについて操作することができます。")
        embed.add_field(name='現在のVCオーナー :',value=after.channel.owner.mention)
        embed.set_footer(text='"</vctool dashboard:973928793154662410>"でダッシュボードを再送信できます')
        self.bot.vc1_dash = await self.bot.vc1.send(embed=embed, view=dashboard(self))
        self.bot.vc1_owner = random.choice(member)
        await after.channel.send(f'{self.bot.vc1_owner.mention}は{after.channel}の所有権を持っています', delete_after=60)


class rename(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="チャンネル名変更",
            timeout=120,
        )
        self.value = None

        self.name = discord.ui.TextInput(
            label="新しいチャンネル名(空白でリセット)",
            style=discord.TextStyle.short,
            placeholder="名前を入力",
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



class status():
    def __init__(self, bot):
        super().__init__()
    async def set(self, channel, status):
        channel.status = status
    
    async def check(self, channel):
        result = channel.status



class select(discord.ui.Select):
    def __init__(self, channel, mode):
        self.option = []
        self.channel = channel
        self.mode = mode
        for user in channel.members:
            self.option.append(discord.SelectOption(label=user.name, value=user.id))
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=self.option)
    async def callback(self, interaction: discord.Interaction):
            for member in self.channel.members:
                if str(member.id) == str(self.values[0]):
                    if self.mode =='kick':
                        try:
                            await member.move_to(None)
                            await interaction.response.send_message(content=f"{member.name}をVCからキックしました",ephemeral=True)
                        except:
                            await interaction.response.send_message(content=f"{member.name}をVCからキックできませんでした",ephemeral=True)
                        break
                    elif self.mode =='owner':
                        await interaction.response.send_message(f'{member.mention}は{self.channel}の所有権を持っています')
                        await interaction.response.send_message(content=f"{member.name}に所有権を移動しました",ephemeral=True)
                        return member
                        view.stop()

class request():
    def __init__(self, channel, bot):
        super().__init__()

    async def sent(self, channel, member):
        embed = discord.Embed(title='VC参加リクエスト', description=f'{member}による参加申請です。\n承諾しますか?')
        await channel.owner.send(embed=embed,view=request_button(self, channel))

class request_button(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
    @discord.ui.button(label='承諾', style=discord.ButtonStyle.green, emoji='✅', row=1)
    async def yes(self, interaction: discord.Interaction, channel, member):
        await member.move_to(channel)
        await interaction.response.send_message('承諾しました')
    @discord.ui.button(label='拒否', style=discord.ButtonStyle.red, emoji='❌', row=1)
    async def yes(self, interaction: discord.Interaction, channel, member):
        await member.move_to(None)
        await interaction.response.send_message('拒否しました')
        await member.send('あなたが申請した参加申請は拒否されました。')

class SelectView(discord.ui.View):
    def __init__(self, channel, mode, *, timeout = 180):
        super().__init__(timeout=timeout)
        member = self.add_item(select(channel, mode))



class dashboard(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
    @discord.ui.button(label='通常モード', style=discord.ButtonStyle.green, emoji='✅', row=1)
    async def normal(self, interaction: discord.Interaction):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == interaction.channel:
            if await status.check(self, interaction.channel) != 'Normal':
                await interaction.channel.edit(sync_permissions=True)
                await status.set(self, interaction.channel, 'Normal')
                await interaction.response.send_message('通常モードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでに通常モードに設定されています', ephemeral=True)
        else:
            await interaction.response.send_message('オーナー以外実行できません', ephemeral=True)
    @discord.ui.button(label='許可モード', style=discord.ButtonStyle.secondary, emoji='📩', row=1)
    async def permit(self, interaction: discord.Interaction):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
                await request.sent
        elif result == 'vc2':
                await interaction.response.send_message('やる気が出たら実装します', ephemeral=True)
        elif result == 'vc3':
                await interaction.response.send_message('やる気が出たら実装します', ephemeral=True)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)

class Vctool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot is False:
            if before.channel != after.channel:
                if before.channel is not None and before.channel:


                    # 通知
                    embed = discord.Embed(title="VC退出", colour=discord.Colour(0xd0021b), description="ユーザーが退出しました", timestamp=datetime.now())

                    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                    embed.set_footer(text="VC入退出通知")

                    await before.channel.send(embed=embed)
            if after.channel.id == 1030990534984081538:
                category = self.bot.guild.get_channel(972144871047577660)
                channel = await self.bot.guild.create_voice_channel(f"{member}の部屋", category=category)
                await member.move_to(channel)
            else:
                if len(after.channel.members) == 1:
                    await owner.setup(self, member, after)
                else:
                    if after.chennel.status == 'Permid':
                        category = self.bot.guild.get_channel(972144871047577660)
                        lobby = await self.bot.guild.create_voice_channel(f'{before.channel}のlobby', category=category)
                        await member.move_to(lobby)


async def setup(bot):
    await bot.add_cog(Vctool(bot))
