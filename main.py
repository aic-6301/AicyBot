import discord
import traceback
import os
import sys
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get('token')
bot = commands.Bot(command_prefix="a!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    bot.guild = bot.get_guild(949560203374915605)
    bot.admin = bot.guild.get_role(1002599926670295152)
    bot.log_ch = bot.get_channel(1004387301293555803)
    kidou = bot.get_channel(1011708105161179136)
    try:
        for file in os.listdir('./cogs'): # cogの中身ロード
            if file.endswith('.py'):
                await bot.load_extension(f'cogs.{file[:-3]}')
                print(f'{file[:-3]}を読み込んだよ!!')
    except:
        traceback.print_exc()
    try:
        for file in os.listdir('./cogs/aicyserver'): # cogs/aicyserverの読み込み
            if file.endswith('.py'):
                await bot.load_extension(f'cogs.aicyserver.{file[:-3]}')
                print(f'{file[:-3]}を読み込んだよ!!')
    except:
        traceback.print_exc()
    try:
        await bot.load_extension('jishaku') # jishakuの読み込み
        print('jishakuを読み込んだよ!!')
    except:
        traceback.print_exc()
    print(f"Logged in as {bot.user}")
    await kidou.send('起動したよ!!')
    guilds=len(bot.guilds)
    servers=str(guilds)
    members = str(guilds.members)
    await bot.change_presence(activity = discord.Activity(name=f"メンバー数:{members}, サーバー数:{servers}", type=discord.ActivityType.playing), status='online')
    bot.vc1 = bot.get_channel(1004606464918298684)
    bot.vc2 = bot.get_channel(1004606505754046514)
    bot.vc3 = bot.get_channel(1004606533176414321)
    bot.vc1_owner = None
    bot.vc2_owner = None
    bot.vc3_owner = None
    bot.vc1_dash = None
    bot.vc2_dash = None
    bot.vc3_dash = None

    bot.vc1_status = 'Normal'
    bot.vc2_status = 'Normal'
    bot.vc3_status = 'Normal'


@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am a robot")

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    embed = discord.Embed(title='Reload!', description=f'{extension} Reloaded!', color=0xff00c8)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    embed = discord.Embed(title='Load!', description=f'{extension} Loaded!', color=0xff00c8)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.send('再起動します。。')
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.event
async def on_command_error(ctx, error):
    error_ch = bot.get_channel(1011469317822496858)
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


bot.run(token)
