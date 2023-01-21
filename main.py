import asyncio
import logging
import os
import sys
import traceback
from dotenv import load_dotenv
import datetime
from datetime import timezone


import disnake
from disnake.ext import commands

load_dotenv()
TOKEN = os.getenv("token")
class AicyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="a!",
            intents=disnake.Intents.all(),
            help_command=None,
            command_sync_flags=commands.CommandSyncFlags.all(),
        )
        self.start_time: datetime = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)

    async def on_ready(self):
        await self.change_presence(activity=disnake.Game(name="あいしぃーぼっと"), status="online")
        try:
            self.load_extension("jishaku")
        except Exception:
            traceback.print_exc()
        for file in os.listdir("./cogs"): # cogs loader
            if file.endswith(".py"):
                try:
                    bot.load_extension(f'cogs.{file[:-3]}')
                    print(f"Loaded cogs: cogs.{file[:-3]}")
                except Exception:
                    traceback.print_exc()
        print(f"Ready! {self.user.name}({self.user.id})")
        await self.get_channel(1058005805426814976).send(embed=disnake.Embed(title="起動しました！", description=f"<t:{self.start_time.timestamp():.0f}:R>にAicyBotが起動しました!\n disnake Version: {disnake.__version__}"))

if __name__ == "__main__":
    bot = AicyBot()
    bot.run(TOKEN)