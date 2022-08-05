import discord
from discord.ext import commands
import sqlite3
import json

conn=sqlite3.connect("level.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS level(userid, level, exp)")

class level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener(name='on_message')
    async def level_count(self, message, member):
        with open('guilds.json', 'r', encoding='utf-8') as f:
            guilds_dict = json.load(f)
        if message.guild.id == guilds_dict:
            if message.author.bot:
                return
            if message.content.startswith('a!'):
                return
            c.execute("SELECT * FROM level WHERE userid=?", (message.author.id,))
            data=c.fetchone()
            if data is None:
                c.execute("INSERT INTO level VALUES(?, ?, ?)",(message.author.id, 1, 0))
                conn.commit()
                return
            c.execute("UPDATE level set exp=? WHERE userid=?",(data[2]+1, message.author.id))
            conn.commit()
            c.execute("SELECT * FROM level WHERE userid=?", (message.author.id,))
            data=c.fetchone()
            if data[2] >= data[1]*5:
                c.execute("UPDATE level set level=?,exp=? WHERE userid=?",(data[1]+1,0,message.author.id))
                conn.commit()
                e = c.execute(title='レベルアップ!', description=f'`a!level`で確認できます!')
                await message.channel.send(embed=e)
    
    @commands.command()
    async def level(self, ctx, target:discord.User=None):
        if target is None:
            user=ctx.author
        else:
            user=target
        c.execute("SELECT * FROM level WHERE userid=?", (user.id,))
        data=c.fetchone()
        if data is None:
            await ctx.send("ユーザーが登録されていません")
        e=discord.Embed(title=f"{user}のランク", description=f"Lv.{data[1]}")
        await ctx.send(embed=e)

    @commands.command()
    async def rank(self, ctx):
        r={}
        title="ランク(トップ3まで)"
        c.execute("SELECT * FROM level")
        for i in c.fetchall():
            user=await self.bot.fetch_user(i[0])
            r[i[1]]=user.name
        rag=[i for i in r]
        rank=sorted(rag, reverse=True)
        b=0
        description="\n".join(f"{r[f]}" for f in rank)
        e=discord.Embed(title=title, description=description)
        await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(level(bot))