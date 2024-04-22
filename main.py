import discord
import requests
from discord.ext import commands

# Import configuration variables
import config

# Bot settings
intents = discord.Intents().all()
client = commands.Bot(command_prefix='$', intents=intents)

# Bot login event
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

# Bot message event
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$weather"):
        city = message.content.split(" ")[1]
        response = requests.get(
            config.api_url,
            params={"q": city, "appid": config.apikey, "units": "metric"}
        )
        
        if response.status_code != 200:
            print(f"API request error: {response.status_code} - {response.text}")
            await message.channel.send(f"API request error: {response.status_code}.")
            return

        data = response.json()
        if data.get("cod") == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            response_message = f"Weather in {city}: {weather_description.capitalize()}, {temperature}°C"
        else:
            response_message = f"Could not fetch weather data for {city}. Reason: {data.get('message', 'Unknown error')}."

        await message.channel.send(response_message)

client.run(config.token)
