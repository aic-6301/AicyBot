import discord
from discord.ext import commands
import random
from discord import app_commands


class owner():
    def __init__(self, bot):
        super().__init__()

    async def setup(self, member, after=None):
        if self.bot.vc1 is None:
            self.bot.vc1 = after.channel
            self.bot.vc1_owner = member
            await after.channel.send(f"{member.mention}が{after.channel.name}のオーナーです", delete_after=120)
            self.bot.vc1_dash = await after.channel.send(view=dashboard(self))
        elif self.bot.vc2 is None:
            self.bot.vc2 = after.channel
            self.bot.vc2_owner = member
            await after.channel.send(f"{member.mention}が{after.channel.name}のオーナーです", delete_after=120)
            self.bot.vc2_dash = await after.channel.send(view=dashboard(self))
        elif self.bot.vc3 is None:
            self.bot.vc3 = after.channel
            self.bot.vc3_owner = member
            await after.channel.send(f"{member.mention}が{after.channel.name}のオーナーです", delete_after=120)
            self.bot.vc3_dash = await after.channel.send(view=dashboard(self))
        elif self.bot.vc4 is None:
            self.bot.vc4 = after.channel
            self.bot.vc4_owner = member
            await after.channel.send(f"{member.mention}が{after.channel.name}のオーナーです", delete_after=120)
            self.bot.vc4_dash = await after.channel.send(view=dashboard(self))
        elif self.bot.vc5 is None:
            self.bot.vc5 = after.channel
            self.bot.vc5_owner = member
            await after.channel.send(f"{member.mention}が{after.channel.name}のオーナーです", delete_after=120)
            self.bot.vc5_dash = await after.channel.send(view=dashboard(self))

    # オーナー変更用
    async def change(self, channel, mode, member=None):
        if mode == "random":
            if channel is self.bot.vc1:
                member = random.choice(channel.members)
                self.bot.vc1_owner = member
                await channel.send(f"{member.mention}が{channel.name}のオーナーです\nダッシュボードを出すには、</vc dashboard:>を実行してください。", delete_after=120)
            elif channel is self.bot.vc2:
                member = random.choice(channel.members)
                self.bot.vc2_owner = member
                await channel.send(f"{member.mention}が{channel.name}のオーナーです\nダッシュボードを出すには、</vc dashboard:>を実行してください。", delete_after=120)
            elif channel is self.bot.vc3:
                member = random.choice(channel.members)
                self.bot.vc3_owner = member
                await channel.send(f"{member.mention}が{channel.name}のオーナーです\nダッシュボードを出すには、</vc dashboard:>を実行してください。", delete_after=120)
            elif channel is self.bot.vc4:
                member = random.choice(channel.members)
                self.bot.vc4_owner = member
                await channel.send(f"{member.mention}が{channel.name}のオーナーです\nダッシュボードを出すには、</vc dashboard:>を実行してください。", delete_after=120)
            elif channel is self.bot.vc5:
                member = random.choice(channel.members)
                self.bot.vc5_owner = member
                await channel.send(f"{member.mention}が{channel.name}のオーナーです\nダッシュボードを出すには、</vc dashboard:>を実行してください。", delete_after=120)



        elif mode == "set":
            if channel is self.bot.vc1:
                self.bot.vc1_owner = member
                await channel.send(f"{member.mention}が{channel.name}のオーナーです\nダッシュボードを出すには、</vc dashboard:>を実行してください。", delete_after=120)
            elif channel is self.bot.vc2:
                self.bot.vc2_owner = member
                await channel.send(f"{member.mention}が{channel.name}のオーナーです\nダッシュボードを出すには、</vc dashboard:>を実行してください。", delete_after=120)
            elif channel is self.bot.vc3:
                self.bot.vc3_owner = member
                await channel.send(f"{member.mention}が{channel.name}のオーナーです\nダッシュボードを出すには、</vc dashboard:>を実行してください。", delete_after=120)
            elif channel is self.bot.vc4:
                self.bot.vc4_owner = member
                await channel.send(f"{member.mention}が{channel.name}のオーナーです\nダッシュボードを出すには、</vc dashboard:>を実行してください。", delete_after=120)
            elif channel is self.bot.vc5:
                self.bot.vc5_owner = member
                await channel.send(f"{member.mention}が{channel.name}のオーナーです\nダッシュボードを出すには、</vc dashboard:>を実行してください。", delete_after=120)



    # オーナーかどうかチェック
    async def check(self, member, channel):
        if channel is self.bot.vc1 and member is self.bot.vc1_owner:
            result = 'vc1'
        elif channel == self.bot.vc2 and member == self.bot.vc2_owner:
            result = 'vc2'
        elif channel == self.bot.vc3 and member == self.bot.vc3_owner:
            result = 'vc3'
        elif channel == self.bot.vc4 and member == self.bot.vc4_owner:
            result = 'vc4'
        elif channel == self.bot.vc5 and member == self.bot.vc5_owner:
            result = 'vc5'
        else:
            result = None
        return result


class status():
    def __init__(self, bot):
        super().__init__()
    
    async def set(self, channel, status):
        if channel == self.bot.vc1:
            self.bot.vc1_status = status
        elif channel == self.bot.vc2:
            self.bot.vc2_status = status
        elif channel == self.bot.vc3:
            self.bot.vc3_status = status
    
    async def check(self, channel):
        if channel == self.bot.vc1:
            result = self.bot.vc1_status
        elif channel == self.bot.vc2:
            result  = self.bot.vc2_status
        elif channel == self.bot.vc3:
            result = self.bot.vc3_status
        return result




class dashboard(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.timeout=None
        self.bot = bot
    @discord.ui.button(label='通常モード', style=discord.ButtonStyle.green, emoji='✅', row=1)
    async def Normal(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        # VC1
        if result == 'vc1':
            if await status.check(self, interaction.channel) != 'Normal':
                await interaction.channel.edit(sync_permissions=True)
                await status.set(self, interaction.channel, 'Normal')
                await interaction.response.send_message('通常モードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでに通常モードに設定されています', ephemeral=True)
        # VC2
        elif result == 'vc2':
            if await status.check(self, interaction.channel) != 'Normal':
                await interaction.channel.edit(sync_permissions=True)
                await status.set(self, interaction.channel, 'Normal')
                await interaction.response.send_message('通常モードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでに通常モードに設定されています', ephemeral=True)
        # VC3
        elif result == 'vc3':
            if await status.check(self, interaction.channel) != 'Normal':
                await interaction.channel.edit(sync_permissions=True)
                await status.set(self, interaction.channel, 'Normal')
                await interaction.response.send_message('通常モードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでに通常モードに設定されています', ephemeral=True)
        elif result == 'vc4':
            if await status.check(self, interaction.channel) != 'Normal':
                await interaction.channel.edit(sync_permissions=True)
                await status.set(self, interaction.channel, 'Normal')
                await interaction.response.send_message('通常モードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでに通常モードに設定されています', ephemeral=True)
        elif result == 'vc5':
            if await status.check(self, interaction.channel) != 'Normal':
                await interaction.channel.edit(sync_permissions=True)
                await status.set(self, interaction.channel, 'Normal')
                await interaction.response.send_message('通常モードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでに通常モードに設定されています', ephemeral=True)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


    @discord.ui.button(label="ロック", style=discord.ButtonStyle.green, emoji="🔒", row=1)
    async def lock(self, button: discord.ui.Button, interaction: discord.Interaction):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            if await status.check(self, interaction.channel) != 'Lock':
                await interaction.channel.edit(sync_permissions=True)
                member = self.bot.vc1.members
                for user in member:
                    await interaction.channel.set_permissions(user, connect=True)
                await interaction.channel.set_permissions(self.bot.everyone, connect=False)
                await interaction.channel.set_permissions(self.bot.bot_role, connect=True)
                await status.set(self, interaction.channel, 'Lock')
                await interaction.response.send_message("ロックしました", ephemeral=True)
            else:
                await interaction.response.send_message("すでにロックされています", ephemeral=True)
        elif result == 'vc2':
            if await status.check(self, interaction.channel) != 'Lock':
                await interaction.channel.edit(sync_permissions=True)
                member = self.bot.vc1.members
                for user in member:
                    await interaction.channel.set_permissions(user, connect=True)
                await interaction.channel.set_permissions(self.bot.everyone, connect=False)
                await interaction.channel.set_permissions(self.bot.bot_role, connect=True)
                await status.set(self, interaction.channel, 'Lock')
                await interaction.response.send_message("ロックしました", ephemeral=True)
            else:
                await interaction.response.send_message("すでにロックされています", ephemeral=True)
        elif result == 'vc3':
            if await status.check(self, interaction.channel) != 'Lock':
                await interaction.channel.edit(sync_permissions=True)
                member = self.bot.vc3.members
                for user in member:
                    await interaction.channel.set_permissions(user, connect=True)
                await interaction.channel.set_permissions(self.bot.everyone, connect=False)
                await interaction.channel.set_permissions(self.bot.bot_role, connect=True)
                await status.set(self, interaction.channel, 'Lock')
                await interaction.response.send_message("ロックしました", ephemeral=True)
            else:
                await interaction.response.send_message("すでにロックされています", ephemeral=True)
        elif result == 'vc4':
            if await status.check(self, interaction.channel) != 'Lock':
                await interaction.channel.edit(sync_permissions=True)
                member = self.bot.vc4.members
                for user in member:
                    await interaction.channel.set_permissions(user, connect=True)
                await interaction.channel.set_permissions(self.bot.everyone, connect=False)
                await interaction.channel.set_permissions(self.bot.bot_role, connect=True)
                await status.set(self, interaction.channel, 'Lock')
                await interaction.response.send_message("ロックしました", ephemeral=True)
            else:
                await interaction.response.send_message("すでにロックされています", ephemeral=True)
        elif result == 'vc5':
            if await status.check(self, interaction.channel) != 'Lock':
                await interaction.channel.edit(sync_permissions=True)
                member = self.bot.vc5.members
                for user in member:
                    await interaction.channel.set_permissions(user, connect=True)
                await interaction.channel.set_permissions(self.bot.everyone, connect=False)
                await interaction.channel.set_permissions(self.bot.bot_role, connect=True)
                await status.set(self, interaction.channel, 'Lock')
                await interaction.response.send_message("ロックしました", ephemeral=True)
            else:
                await interaction.response.send_message("すでにロックされています", ephemeral=True)
        

class Vc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    group = app_commands.Group(name="vc", description="VC関係のコマンド", guild_ids=['981800095760670730'], guild_only=True)

    @group.command(name="dashboard", description="ダッシュボードを表示します")
    async def dashboard(self, interaction: discord.Interaction):
        await print()
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # 大量定義広場
        #TODO: 別のところに定義する
        category = self.bot.guild.get_channel(1063711277425377310)
        create_channel = self.bot.guild.get_channel(1064177214603661353)
        afk = self.bot.guild.get_channel(1063711300015898675)
        count_channel = self.bot.guild.get_channel(1064458492733313044)
        stage = self.bot.guild.get_channel(1063711289521733662)

        # vcの数を数える
        #TODO: もう少し簡略化したい
        voice_count = category.voice_channels
        vc_count = 0
        for ch in category.voice_channels:
            if ch is afk:
                voice_count.pop(vc_count)
                vc_count-=1
            if ch is create_channel:
                voice_count.pop(vc_count)
                vc_count-=1
            if ch is count_channel:
                voice_count.pop(vc_count)
                vc_count-=1
            vc_count+=1


        if member.bot is False: # botを除く
            if vc_count is not int(self.bot.config['vc_count']): # configの値じゃないか
                if before.channel != after.channel: # 入退室のみ

                    # 作成機構
                    if after.channel == create_channel: # 入室したチャンネルが作成チャンネルか
                        created_vc = await category.create_voice_channel(name=f"{member.name}の部屋")
                        await member.move_to(created_vc)
                        await created_vc.send(f"{member.name}さんの部屋ができました。")
                        await owner.setup(self, member, after)

            # 拒否機構(?)
            elif vc_count == int(self.bot.config['vc_count']):
                await member.move_to(None) # メンバーを退出させる
                await member.send(f"現在VCチャンネルの数が{self.bot.config['vc_count']}つまでと制限されています。\n申し訳ございませんが、現在作られているチャンネルにご参加ください。\n now:{vc_count}\n config:{self.bot.config['vc_count']}") # dmを送信



            # botを除く
            vcmembers = before.channel.members
            count = 0
            for m in before.channel.members:
                if m.bot == True:
                    vcmembers.pop(count)
                    count -= 1
                count += 1
                # 退出時、作成チャンネル,afkかステージじゃないか
                if before.channel is not None and before.channel is not create_channel or afk or stage:
                    if len(vcmembers) == 0: # botを除いたメンバーが0人か
                        await before.channel.delete()



                    # 退出時、オーナーかどうかチェック
                    else:
                        if await owner.check(self, member, before.channel) != None:
                            await owner.change(self, before.channel, mode="random")

async def setup(bot):
    await bot.add_cog(Vc(bot))