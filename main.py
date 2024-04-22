import discord
import requests
import config
from discord.ext import commands

channel = config.channelid
key = config.apikey
url = config.api_url

intents = discord.Intents().all()
client = commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$weather"):
        city = message.content.split(" ")[1]
        response = requests.get(
            url,
            params={"q": city, "appid": url, "units": "metric"}
        )
        data = response.json()

        if data.get("cod") == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            response_message = f"Weather in {city}: {weather_description.capitalize()}, {temperature}°C"
        else:
            response_message = f"Could not fetch weather data for {city}."

        await message.channel.send(response_message)

client.run(config.token) 