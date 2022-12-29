import discord
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

def eew_embed(response):
    body = response['Body']
    head = response['head']
    color = eew_color(body)
    eew_image()
    embed = discord.Embed(title="地震情報",
    description=f"{head['Headline']}{body['Comments']['Observation']}\n震源の深さは{body['Earthquake']['Hypocenter']['Depth']}km地震の規模はM{body['Earthquake']['Magnitude']}と推定されています。",
    color=color,
    timestamp=datetime.now())
    embed.set_image(url='attachment://image.png')
    embed.set_footer(text=f"情報元：{response['Control']['PublishingOffice']}")
    return embed


def eew_color(body):
    if body['Intensity']['Observation']['MaxInt'] == "1":
        color = discord.Color.from_rgb(60, 90, 130)
    elif body['Intensity']['Observation']['MaxInt'] == "2":
        color = discord.Color.from_rgb(30, 130, 230)
    elif body['Intensity']['Observation']['MaxInt'] == "3":
        color = discord.Color.from_rgb(120, 230, 220)
    elif body['Intensity']['Observation']['MaxInt'] == "4":
        color = discord.Color.from_rgb(255, 255, 150)
    elif body['Intensity']['Observation']['MaxInt'] == "5-":
        color = discord.Color.from_rgb(255, 210, 0)
    elif body['Intensity']['Observation']['MaxInt'] == "5+":
        color = discord.Color.from_rgb(255, 150, 0)
    elif body['Intensity']['Observation']['MaxInt'] == "6-":
        color = discord.Color.from_rgb(240, 50, 0)
    elif body['Intensity']['Observation']['MaxInt'] == "6+":
        color = discord.Color.from_rgb(190, 0, 0)
    elif body['Intensity']['Observation']['MaxInt'] == "7":
        color = discord.Color.from_rgb(140, 0, 40)
    return color

def eew_image():
    driver = webdriver.Chrome('./chromedriver')
    url = 'https://ntool.online/weather/earthquake?fullscreen=true'
    driver.get(url)
    driver.set_window_size(960, 540)
    driver.save_screenshot("image.png")
    driver.quit()
    return