import discord
import requests
import config

token = config.token
channel = config.channelid
key = config.apikey
url = config.api_url

client = discord.Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
