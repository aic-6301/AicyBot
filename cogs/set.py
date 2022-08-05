import discord
import json
from discord.ext import commands


class set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def set(self, ctx):
        e = discord.Embed(title='`set`', description='``')
        e.add_field(name='level', description='レベリング機能を設定します')
        e.add_field(name='追加中...', description='他の設定も追加中です...')
        await ctx.send(embed=e)

    @set.command()
    async def set_level(self, ctx):
        with open('guilds.json', 'r', encoding='utf-8') as f:
            guilds_dict = json.load(f)

        guilds_dict[str(ctx.guild.id)]
        with open('guilds.json', 'w', encoding='utf-8') as f:
            json.dump(guilds_dict, f, indent=4, ensure_ascii=False)
    
        await ctx.send(f'レベリング機能をONにしました')

async def setup(bot):
    await bot.add_cog(set(bot))
