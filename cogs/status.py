import discord
from discord.ext import commands, tasks
import requests
import json
from datetime import datetime


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status.start()

    @tasks.loop(minutes=3)
    async def status(self):
        await self.bot.change_presence(activity = discord.Activity(name=f"Server Running! 最終更新：{datetime.now().strftime('%H:%M')} | メンバー数:{len(self.bot.users)}", type=discord.ActivityType.streaming), status='idle')
        try:
            uri = requests.get("https://api.aic-group.net/get/status")
            text = uri.text
            data = json.loads(text)
            self.message = None
            try:
                self.message.delete()
            except:
                pass
        except:
            if self.message != None:
                self.message = await self.bot.guild.system_channel.send('サーバーからステーサスが取得できませんでした。\nOSフリーズまたはip変更の時間の可能性があります。')
        e = discord.Embed(title="各ステータス", color=discord.Colour.from_rgb(160, 106, 84), timestamp=datetime.now())
        e.clear_fields
        if (data['MainSite']) == 'OK':
            e.add_field(name="メインサイト", value='✅オンライン\n[サイトに行く](https://www.aic-group.net)')
        else:
            e.add_field(name="メインサイト", value='❌オフライン')
        if (data['AicyBlog']) == 'OK':
            e.add_field(name="ブログ", value='✅オンライン\n[サイトに行く](https://blog.aic-group.net)')
        else:
            e.add_field(name="ブログ", value='❌オフライン')
        if (data['AicyWiki']) == 'OK':
            e.add_field(name="Wiki", value='✅オンライン\n[サイトに行く](https://wiki.aic-group.net)')
        else:
            e.add_field(name="Wiki", value='❌オフライン')
        if (data['AicyAPI']) == 'OK':
            e.add_field(name="API", value='✅オンライン')
        else:
            e.add_field(name="API", value='❌オフライン')
        if (data['AicyMedia']) == 'OK':
            e.add_field(name="Media", value='✅オンライン\n[サイトに行く](https://media.aic-group.net)')
        else:
            e.add_field(name="Media", value='❌オフライン')
        if (data['AicyLive']) == 'OK':
            e.add_field(name="Live", value='✅オンライン\n[サイトに行く](https://live.aic-group.net)')
        else:
            e.add_field(name="Live", value='❌オフライン')
        if (data['AicyGit']) == 'OK':
            e.add_field(name="Git", value='✅オンライン\n[サイトに行く](https://git.aic-group.net)')
        else:
            e.add_field(name="Git", value='❌オフライン')
        if (data['Minecraft Server']) == 'OK':
            e.add_field(name="Minecraft", value='✅オンライン')
        else:
            e.add_field(name="Minecraft", value='❌オフライン')
        
        msg = await self.bot.get_channel(1030355963586289774).fetch_message(1034089953413570631)
        await msg.edit(embed=e)

async def setup(bot):
    await bot.add_cog(Status(bot))
