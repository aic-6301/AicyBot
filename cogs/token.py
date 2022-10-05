import asyncio
import base64
import os
import re
import textwrap

import aiohttp
import discord
from discord.ext import commands


class token(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    TOKEN_PATTERN = re.compile(
        r"([0-9a-zA-Z\-_]{24})\.[0-9a-zA-Z\-_]{6,7}\.[0-9a-zA-Z\-_]{27}"
    )
    token_cache = []

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        TOKEN_PATTERN = re.compile(
            r"([0-9a-zA-Z\-_]{24})\.[0-9a-zA-Z\-_]{6,7}\.[0-9a-zA-Z\-_]{27}"
        )
        token_cache = []
        for t in TOKEN_PATTERN.finditer(message.content):
            u = int(base64.urlsafe_b64decode(t[1]))
            try:
                user = await self.bot.fetch_user(u)
            except discord.errors.NotFound:
                pass
            else:
                token = message.content
                if token not in token_cache:
                    token_cache.append(token)
                    token_text = textwrap.dedent(
                        f"""
                        {user}'s token has been leaked!
                        {token}
                        
                        Guild:
                            {message.guild}
                        
                        Channel:
                            {message.channel}
                        
                        User:
                            {message.author}
                        
                        URL:
                            {message.jump_url}
                        
                        Make sure your token isn't public.
                        This Gist will be deleted in 5 minutes.
                        by No name. is using your code.
                        """
                    )
                    token_text_ja = textwrap.dedent(
                        f"""
                        {user}のトークンが漏れてしまいました！
                        {token}
                        
                        サーバー：
                            {message.guild.name}
                        
                        チャンネル：
                            {message.channel.name}
                        
                        ユーザー：
                            {message.author}
                        
                        URL：
                            {message.jump_url}
                        
                        トークンが見える状況ではないか確かめて下さい。
                        このGistは5分で削除されます。
                        by名無し。さんのコードを流用しています。
                        """
                    )
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            "https://api.github.com/gists",
                            headers={
                                "authorization": "token "
                                + "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",
                                "accept": "application/json",
                            },
                            json={
                                "files": {
                                    "token_en.txt": {"content": token_text},
                                    "token_ja.txt": {"content": token_text_ja},
                                },
                                "public": True,
                            },
                        ) as gist_response:
                            if gist_response.status == 201:
                                await message.reply(
                                    f"**{user}'s token has been leaked!**\nToken has been disabled because we've uploaded token to gist, but please don't leak token more!\n\n**{user}のトークン漏れを検知しました！**\nGistにアップロードしたためトークンは無効化されましたが、公開しないように気をつけて下さい！"
                                )
                                await message.add_reaction("🔐")
                                gist_id = (await gist_response.json())["id"]
                            else:
                                return
                    await asyncio.sleep(120)
                    async with aiohttp.ClientSession() as session:
                        async with session.delete(
                            "https://api.github.com/gists/" + gist_id,
                            headers={
                                "authorization": "token " + os.getenv("github_token")
                            },
                        ) as gist_response:
                            pass

        for a in message.attachments:
            for t in TOKEN_PATTERN.finditer(str(await a.read())):
                u = int(base64.urlsafe_b64decode(t[1]))
                try:
                    user = await self.bot.fetch_user(u)
                except discord.errors.NotFound:
                    pass
                else:
                    token = message.content
                    if token not in token_cache:
                        token_cache.append(token)
                        token_text = textwrap.dedent(
                            f"""
                            {user}'s token has been leaked!
                            {token}
                            
                            Guild:
                                {message.guild}
                            
                            Channel:
                                {message.channel}
                            
                            User:
                                {message.author}
                            
                            URL:
                                {message.jump_url}
                            
                            Make sure your token isn't public.
                            This Gist will be deleted in 5 minutes.
                            by No name. is using your code.
                            """
                        )
                        token_text_ja = textwrap.dedent(
                            f"""
                            {user}のトークンが漏れてしまいました！
                            {token}
                            
                            サーバー：
                                {message.guild.name}
                            
                            チャンネル：
                                {message.channel.name}
                            
                            ユーザー：
                                {message.author}
                            
                            URL：
                                {message.jump_url}
                            
                            トークンが見える状況ではないか確かめて下さい。
                            このGistは5分で削除されます。
                            by名無し。さんのコードを流用しています。
                            """
                        )
                        async with aiohttp.ClientSession() as session:
                            async with session.post(
                                "https://api.github.com/gists",
                                headers={
                                    "authorization": "token "
                                    + "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",
                                    "accept": "application/json",
                                },
                                json={
                                    "files": {
                                        "token_en.txt": {"content": token_text},
                                        "token_ja.txt": {"content": token_text_ja},
                                    },
                                    "public": True,
                                },
                            ) as gist_response:
                                if gist_response.status == 201:
                                    await message.reply(
                                        f"**{user}'s token has been leaked!**\nToken has been disabled because we've uploaded token to gist, but please don't leak token more!\n\n**{user}のトークン漏れを検知しました！**\nGistにアップロードしたためトークンは無効化されましたが、公開しないように気をつけて下さい！"
                                    )
                                    await message.add_reaction("🔐")
                                    gist_id = (await gist_response.json())["id"]
                                else:
                                    return
                        await asyncio.sleep(120)
                        async with aiohttp.ClientSession() as session:
                            async with session.delete(
                                "https://api.github.com/gists/" + gist_id,
                                headers={
                                    "authorization": "token "
                                    + "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"
                                },
                            ) as gist_response:
                                pass


async def setup(bot):
    await bot.add_cog(token(bot))
