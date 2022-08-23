import discord
from datetime import timedelta
from discord.ext import commands
import asyncio
import datetime


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def mod(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title='`mod`のサブコマンド', description='管理向け')
            e.add_field(name='`setup`', value='moderationのセットアップをします')
            e.add_field(name='`ban`', value='メンバーをbanします(idのみ対応)')
            ctx.send(embed=e)
    # setup
    @mod.command(name='setup')
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        if discord.utils.get(ctx.message.server.roles, name='Muted') is None:
            log_ch = self.bot.get_channel(1004387301293555803)
            guild = ctx.guild
            embed = discord.Embed(title='Setup', description='moderationのセットアップをしています')
            embed.add_field(name='□ロールの設定をしています', value='Creating')
            e = discord.Embed(title='Setup', description='moderationのセットアップをしています')
            e.add_field(name='✅ロールの設定をしています', value='Created Muted role!', inline=False)
            e.add_field(name='□ロールの権限の設定をしています', value='resetting', inline=False)
            em = discord.Embed(title='Setup', description='サーバーののセットアップをしています')
            em.add_field(name='✅ロールの設定をしています', value='Created Muted role!', inline=False)
            em.add_field(name='✅ロールの権限の設定をしています', value='configured ' , inline=False)
            em.add_field(name='□サーバーセットアップを終わらせています。。', value='あと少しです。。。', inline=False)
            emb = discord.Embed(title='Setup', description='サーバーのセットアップをしています')
            emb.add_field(name='✅ロールの設定をしています', value='Created Muted role!', inline=False)
            emb.add_field(name='✅ロールの権限の設定をしています', value='configured ', inline=False)
            emb.add_field(name='✅サーバーセットアップを終わらせています。。', value='Done.', inline=False)
            emb.add_field(name='✅サーバーセットアップが終了しました!', value='これで正常にmoderation機能が使えるはずです!', inline=False)
            emb.set_footer(text='この機能はβ版です。エラーが発生した場合はBot管理者までお問い合わせください。')
            msg = await ctx.send(embed=embed)
            msg = await msg.edit(embed=e)
            perms = discord.Permissions(send_messages=False, read_messages=True)
            await guild.create_role(name='Muted', permissions=perms)
            msg = await msg.edit(embed=em)
            server = discord.Embed(title='サーバー通知', description='サーバーセットアップ時の通知です')
            server.add_field(name='サーバー名', value=guild.name, inline=True)
            server.add_field(name='サーバーid', value=guild.id, inline=True)
            server.add_field(name='サーバーオーナー', value=guild.owner, inline=True)
            server.add_field(name='サーバー作成日', value=guild.created_at, inline=True)
            await log_ch.send(embed=server)
            msg = await msg.edit(embed=emb)
        else:
            embed = discord.Embed(title='セットアップ済みのようです', description='こちらのサーバーでは実行する必要はありません！')
    
    # ban
    @mod.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def ban(self, ctx, member_id: int, *, reason):
        member = ctx.guild.get_member(member_id)
        e = discord.Embed(title='Banned', color=0xff0000)
        e.add_field(name="メンバー", value=f"{member.mention}", inline=False)
        e.add_field(name="理由", value=f"{reason}", inline=False)
        await member.ban(delete_message_days=7, reason=reason)
        embed=discord.Embed(title="BAN", color=0xff0000)
        embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
        embed.add_field(name="理由", value=f"{reason}", inline=False)
        await member.send(embed=e)
        await ctx.send(embed=embed)
    # unban
    @mod.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def unban(self, ctx, member_id: int, *, reason):
        member = ctx.guild.get_member(member_id)
        e = discord.Embed(title='Unbanned', color=0xff0000)
        e.add_field(name="メンバー", value=f"{member.mention}", inline=False)
        e.add_field(name="理由", value=f"{reason}", inline=False)
        await member.unban(delete_message_days=7, reason=reason)
        embed=discord.Embed(title="Unbanned", color=0xff0000)
        embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
        embed.add_field(name="理由", value=f"{reason}", inline=False)
        await ctx.send(embed=embed)
        await member.send(embed=e)

    #Kickコマンドのコード
    @mod.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(manage_roles=True, kick_members=True)
    async def kick(self, ctx, member:discord.Member, reason):
        e = discord.Embed(title='Kicked', color=0xff0000)
        e.add_field(name="メンバー", value=f"{member.mention}", inline=False)
        e.add_field(name="理由", value=f"{reason}", inline=False)
        await member.kick(reason=reason)
        embed=discord.Embed(title="KICK", color=0xff0000)
        embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
        embed.add_field(name="理由", value=f"{reason}", inline=False)
        await ctx.send(embed=embed)
        await member.send(embed=e)

    # timeout
    @mod.command
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(moderate_members = True)
    async def timeout(self, ctx, member: discord.Member, reason:str): #setting each value with a default value of 0 reduces a lot of the code
        if member.id == ctx.author.id: # 自分かどうか確認
            await ctx.respond("自分をタイムアウトすることは不可です")
            return
        if member.guild_permissions.moderate_members: # 権限もちか確認
            await ctx.respond("運営をタイムすることは不可です。")
            return
        if reason == None:
            await member.timeout_for()
            embed=discord.Embed(title="timeout", color=0xff0000)
            embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
            embed.add_field(name="理由", value=f"なし", inline=False)
            # embed.add_field(name='期間', value=f'{days}日{hours}時間{minutes}分')
            await ctx.respond(embed=embed)
        else:
            await member.timeout_for( reason = reason)
            embed=discord.Embed(title="timeout", color=0xff0000)
            embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
            embed.add_field(name="理由", value=f"{reason}", inline=False)
            # embed.add_field(name='期間', value=f'{days}日{hours}時間{minutes}分')
            await ctx.respond(embed=embed)

    # untimeout
    @mod.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(moderate_members = True)
    async def untimeout(self, ctx, member: discord.Member, reason: str):
        if reason == None:
            await member.remove_timeout()
            embed=discord.Embed(title="untimeout", color=0xff0000)
            embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
            embed.add_field(name="理由", value=f"なし", inline=False)
            await ctx.respond(embed=embed)
        else:
            await member.remove_timeout(reason = reason)
            embed=discord.Embed(title="untimeout", color=0xff0000)
            embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
            embed.add_field(name="理由", value=f"{reason}", inline=False)
            await ctx.respond(embed=embed)
    # mute
    @mod.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def mute(self, ctx, member: discord.Member, time, d, reason=None):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        await member.add_roles(role)
        embed = discord.Embed(title="Muted!", description=f"{member.mention}はミュートされました",colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="理由:", value=reason, inline=False)
        embed.add_field(name="ミュート解除まで:", value=f"{time}{d}", inline=False)
        await ctx.reply(embed=embed)
        if d == "s":
            await asyncio.sleep(int(time))
        if d == "m":
            await asyncio.sleep(int(time*60))
        if d == "h":
            await asyncio.sleep(int(time*60*60))
        if d == "d":
            await asyncio.sleep(int(time*60*60*24))
        await member.remove_roles(role)
        embed = discord.Embed(title="Unmuted", description=f"{member.mention}はミュート解除されました ", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed)

    # unmute
    @mod.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedRole)
        await member.send(f"あなたは {ctx.guild.name}からミュートを解除されました!")
        embed = discord.Embed(title="Unmute", description=f" {member.mention}はミュートを解除されました", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed)
async def setup(bot):
    await bot.add_cog(Mod(bot))
