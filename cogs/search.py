import discord
from discord.ext import commands
import spotipy
import pytube


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="search", with_app_command=True)
    async def search(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.not_found(ctx)
    
    @search.command(name="spotify", description="Spotifyで検索を行います")
    async def spotify(self, ctx, text):
        result = self.bot.spotify.search(q=text, limit=5, offset=0, market='JP')
        names=[]
        links=[]
        embed = discord.Embed(title="検索結果").set_author(name="Spotify", url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/571e5943-4616-4654-bf99-10b3c98f8686/d98301o-426f05ca-8fe5-4636-9009-db9dd1fca1f3.png")
        for r in result["tracks"]:
            embed.add_field(name=r["href"]["items"]["album"]["artists"]["name"], value=f'[再生リンク]({r["href"]["items"]["album"]["artists"]["external_urls"]["spotify"]})')
        await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Search(bot))
