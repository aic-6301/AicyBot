import discord
import json
import requests

def eew_embed(response):
    data = response['earthquake']
    hypocenter = data['hypocenter']
    embed=discord.Embed(title="地震情報", color=discord.Colour.from_rgb(160, 106, 84))
    embed.add_field(name="震源地",value=hypocenter['name'],inline=False)
    embed.add_field(name="最大震度",value=round(data['maxScale']/10),inline=False)
    embed.add_field(name="発生時刻",value=data['time'],inline=False)
    embed.add_field(name="マグニチュード",value=hypocenter['magnitude'],inline=False)
    embed.add_field(name="震源の深さ",value=f"{hypocenter['depth']}Km",inline=False)
    embed.set_footer(text="P2P地震情報API")
    return embed