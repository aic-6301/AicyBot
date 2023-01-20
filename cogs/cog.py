import discord
from discord.ext import commands
import traceback

class test(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.timeout=None
        self.bot = bot

    @discord.ui.button(label="aaa", emoji="ℹ️", style=discord.ButtonStyle.green)
    async def test_callback(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.send_message("やあ！")

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
            error_ch = self.bot.get_channel(1033496616130334784)
            if isinstance(error, discord.ext.commands.errors.MissingPermissions):
                embed = discord.Embed(title=":x: 失敗 -MissingPermissions", description=f"実行者の必要な権限が無いため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
                embed.set_footer(text="お困りの場合はBot管理者までお問い合わせください")
                await ctx.send(embed=embed)
                e = discord.Embed(title='エラー情報', description='',  timestamp=ctx.message.created_at, color=discord.Colour.red())
                e.add_field(name='エラーが発生したサーバー', value=ctx.message.guild.name, inline=False)
                e.add_field(name='エラーが発生したチャンネル', value=ctx.message.channel.name, inline=False)
                e.add_field(name='エラーid', value=ctx.message.id, inline=False)
                e.add_field(name='エラーが発生したコマンド', value=ctx.message.content, inline=False)
                e.add_field(name='エラーを発生させた人', value=ctx.author, inline=False)
                e.add_field(name='エラー内容', value=error, inline=False)
                await error_ch.send(embed=e)
            elif isinstance(error, discord.ext.commands.errors.NotOwner):
                embed = discord.Embed(title=":x: 失敗 -MissingPermissions", description=f"実行者の必要な権限が無いため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
                embed.set_footer(text="お困りの場合はBot管理者までお問い合わせください")
                await ctx.send(embed=embed)
                e = discord.Embed(title='エラー情報', description='',  timestamp=ctx.message.created_at, color=discord.Colour.red())
                e.add_field(name='エラーが発生したサーバー', value=ctx.message.guild.name, inline=False)
                e.add_field(name='エラーが発生したチャンネル', value=ctx.message.channel.name, inline=False)
                e.add_field(name='エラーid', value=ctx.message.id, inline=False)
                e.add_field(name='エラーが発生したコマンド', value=ctx.message.content, inline=False)
                e.add_field(name='エラーを発生させた人', value=ctx.author, inline=False)
                e.add_field(name='エラー内容', value=error, inline=False)
                await error_ch.send(embed=e)
            elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
                embed = discord.Embed(title=":x: 失敗 -BotMissingPermissions", description=f"Botの必要な権限が無いため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
                embed.set_footer(text="お困りの場合はBot管理者までお問い合わせください")
                await ctx.send(embed=embed)
                e = discord.Embed(title='エラー情報', description='',  timestamp=ctx.message.created_at, color=discord.Colour.red())
                e.add_field(name='エラーが発生したサーバー', value=ctx.message.guild.name, inline=False)
                e.add_field(name='エラーが発生したチャンネル', value=ctx.message.channel.name, inline=False)
                e.add_field(name='エラーid', value=ctx.message.id, inline=False)
                e.add_field(name='エラーが発生したコマンド', value=ctx.message.content, inline=False)
                e.add_field(name='エラーを発生させた人', value=ctx.author, inline=False)
                e.add_field(name='エラー内容', value=error, inline=False)
                await error_ch.send(embed=e)
            elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
                embed = discord.Embed(title=":x: 失敗 -CommandNotFound", description=f"不明なコマンドもしくは現在使用不可能なコマンドです。", timestamp=ctx.message.created_at, color=discord.Colour.red())
                embed.set_footer(text="お困りの場合はBot管理者までお問い合わせください")
                await ctx.send(embed=embed)
                e = discord.Embed(title='エラー情報', description='',  timestamp=ctx.message.created_at, color=discord.Colour.red())
                e.add_field(name='エラーが発生したサーバー', value=ctx.message.guild.name, inline=False)
                e.add_field(name='エラーが発生したチャンネル', value=ctx.message.channel.name, inline=False)
                e.add_field(name='エラーid', value=ctx.message.id, inline=False)
                e.add_field(name='エラーが発生したコマンド', value=ctx.message.content, inline=False)
                e.add_field(name='エラーを発生させた人', value=ctx.author, inline=False)
                e.add_field(name='エラー内容', value=error, inline=False)
                await error_ch.send(embed=e)
            elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
                embed = discord.Embed(title=":x: 失敗 -MemberNotFound", description=f"指定されたメンバーが見つかりません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
                embed.set_footer(text="お困りの場合はBot管理者までお問い合わせください")
                await ctx.send(embed=embed)
                e = discord.Embed(title='エラー情報', description='',  timestamp=ctx.message.created_at, color=discord.Colour.red())
                e.add_field(name='エラーが発生したサーバー', value=ctx.message.guild.name, inline=False)
                e.add_field(name='エラーが発生したチャンネル', value=ctx.message.channel.name, inline=False)
                e.add_field(name='エラーid', value=ctx.message.id, inline=False)
                e.add_field(name='エラーが発生したコマンド', value=ctx.message.content, inline=False)
                e.add_field(name='エラーを発生させた人', value=ctx.author, inline=False)
                e.add_field(name='エラー内容', value=error, inline=False)
                await error_ch.send(embed=e)
            elif isinstance(error, discord.ext.commands.errors.BadArgument):
                embed = discord.Embed(title=":x: 失敗 -BadArgument", description=f"指定された引数がエラーを起こしているため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
                embed.set_footer(text="お困りの場合はBot管理者までお問い合わせください")
                await ctx.send(embed=embed)
                e = discord.Embed(title='エラー情報', description='',  timestamp=ctx.message.created_at, color=discord.Colour.red())
                e.add_field(name='エラーが発生したサーバー', value=ctx.message.guild.name, inline=False)
                e.add_field(name='エラーが発生したチャンネル', value=ctx.message.channel.name, inline=False)
                e.add_field(name='エラーid', value=ctx.message.id, inline=False)
                e.add_field(name='エラーが発生したコマンド', value=ctx.message.content, inline=False)
                e.add_field(name='エラーを発生させた人', value=ctx.author, inline=False)
                e.add_field(name='エラー内容', value=error, inline=False)
                await error_ch.send(embed=e)
            elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
                embed = discord.Embed(title=":x: 失敗 -BadArgument", description=f"指定された引数が足りないため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
                embed.set_footer(text="お困りの場合はBot管理者までお問い合わせください")
                await ctx.send(embed=embed)
                e = discord.Embed(title='エラー情報', description='',  timestamp=ctx.message.created_at, color=discord.Colour.red())
                e.add_field(name='エラーが発生したサーバー', value=ctx.message.guild.name, inline=False)
                e.add_field(name='エラーが発生したチャンネル', value=ctx.message.channel.name, inline=False)
                e.add_field(name='エラーid', value=ctx.message.id, inline=False)
                e.add_field(name='エラーが発生したコマンド', value=ctx.message.content, inline=False)
                e.add_field(name='エラーを発生させた人', value=ctx.author, inline=False)
                e.add_field(name='エラー内容', value=error, inline=False)
                await error_ch.send(embed=e)
            else:
                embed = discord.Embed(title=":x: 失敗", description=f'不明なエラーが発生しました', timestamp=ctx.message.created_at, color=discord.Colour.red())
                embed.add_field(name='お問い合わせの際', value=f'お問い合わせる際にはこちらのidもお持ちください。{ctx.message.id}')
                embed.set_footer(text="お困りの場合はBot管理者までお問い合わせください")
                await ctx.send(embed=embed)
                e = discord.Embed(title='エラー情報', description='',  timestamp=ctx.message.created_at, color=discord.Colour.red())
                e.add_field(name='エラーが発生したサーバー', value=ctx.message.guild.name, inline=False)
                e.add_field(name='エラーが発生したチャンネル', value=ctx.message.channel.name, inline=False)
                e.add_field(name='エラーid', value=ctx.message.id, inline=False)
                e.add_field(name='エラーが発生したコマンド', value=ctx.message.content, inline=False)
                e.add_field(name='エラーを発生させた人', value=ctx.author, inline=False)
                e.add_field(name='エラー内容', value=error, inline=False)
                await error_ch.send(embed=e)
                orig_error = getattr(error, "original", error)
                error_msg  = ''.join(traceback.TracebackException.from_exception(orig_error).format())
                await error_ch.send('エラー全文')
                await error_ch.send(error_msg)
    
    @commands.command()
    async def test_button(self, ctx):
        await ctx.send("button test", view=discord.ui.button(label="aaa", emoji="ℹ️", style=discord.ButtonStyle.green, custom_id='test_button'))


@commands.Cog.listener()
async def on_interaction(inter:discord.Interaction):
    if inter

async def setup(bot):
    await bot.add_cog(Cog(bot))
