from motor import motor_asyncio as motor
import discord
import traceback
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get('token')
bot = commands.Bot(command_prefix="a!", intents=discord.Intents.all())
dbclient = motor.AsyncIOMotorClient("mongodb+srv://aicy:dD4gei2qMFZVoTM4@aicy1.z7ime.mongodb.net/?retryWrites=true&w=majority")
db = dbclient["ProfileBot"]
profiles_collection = db.profiles

@bot.event
async def on_ready():
    bot.guild = bot.get_guild(984807772333932594)
    bot.admin = bot.guild.get_role(1002599926670295152)
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')
            print(f'{file[:-3]}を読み込んだよ!!')
    for file in os.listdir('./cogs/aicyserver'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.aicyserver.{file[:-3]}')
            print(f'{file[:-3]}を読み込んだよ!!')
    try:
        await bot.load_extension('jishaku')
        print('jishakuを読み込んだよ!!')
    except:
        traceback.print_exc()
    print(f"Logged in as {bot.user}")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am a robot")

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    admin = bot.admin
    if admin is not None:
        await bot.reload_extension(f'cogs.{extension}')
        embed = discord.Embed(title='Reload!', description=f'{extension} Reloaded!', color=0xff00c8)
        await ctx.send(embed=embed)
    else:
        await ctx.send('このコマンドはbot管理者だけやで')

@bot.command(name="set")
async def set_profile(ctx, *, text):
    new_data = {
        "userid": ctx.author.id,
        "text": text
    }
    result = await profiles_collection.replace_one({
        "userid": ctx.author.id
    }, new_data)
    if result.matched_count == 0:
        await profiles_collection.insert_one(new_data)
    await ctx.reply("設定が完了しました。")


@bot.command(name="show")
async def show_profile(ctx, target: discord.User):
    profile = await profiles_collection.find_one({
        "userid": target.id
    }, {
        "_id": False
    })
    if profile is None:
        return await ctx.reply("見付かりませんでした。")
    embed = discord.Embed(title=f"`{target}`のプロフィール", description=profile["text"])
    return await ctx.reply(embed=embed)


@bot.command(name="delete", aliases=["del"])
async def delete_profile(ctx):
    result = await profiles_collection.delete_one({
        "userid": ctx.author.id
    })
    if result.deleted_count == 0:
        return await ctx.reply("見付かりませんでした。")
    return await ctx.reply("削除しました。")

@bot.event
async def on_command_error(ctx, error):
    error_ch = bot.get_channel(996370412239855667)
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
        e = discord.Embed(title='エラー情報', description='',  timestamp=ctx.message.created_at, color=discord.Colour.red())
        e.add_field(name='エラーが発生したサーバー', value=ctx.message.guild.name, inline=False)
        e.add_field(name='エラーが発生したチャンネル', value=ctx.message.channel.name, inline=False)
        e.add_field(name='エラーid', value=ctx.message.id, inline=False)
        e.add_field(name='エラーが発生したコマンド', value=ctx.message.content, inline=False)
        e.add_field(name='エラーを発生させた人', value=ctx.author, inline=False)
        e.add_field(name='エラー内容', value=error, inline=False)
        await error_ch.send(embed=e)
        raise error


bot.run(token)
