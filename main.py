import discord
import requests 
import os
from dotenv import load_dotenv, find_dotenv
import datetime 


# Discord Intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Discord Token
load_dotenv(find_dotenv())
bot_token = os.getenv('TOKEN')

# API_KEY
API_KEY = "insert Open Weather API KEY here"


def info(data):
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    country = data['sys']['country']
    description = data['weather'][0]['description']

    all_data = (f"Country : {country}\n" + f"Current Temperature : {temp}°C\n" + f"Currently Feels like : {feels_like}°C\n" + f"Description : {description}\n")
    return all_data


#Startup event
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game("?help"))

# User events
@client.event
async def on_message(message):

    # Help
    if message.content.startswith("?help"):
        embed = discord.Embed(
                title="COMMANDS",
                description="Do $ + the city, country initals \nExample : ?London, GB",
                colour = 0x3498DB,
                timestamp=datetime.datetime.utcnow()
        )

        embed.set_author(name="WEATHER BOT", icon_url="https://media.discordapp.net/attachments/1081590091182510220/1081905211787989003/weather2.png?width=469&height=469")
        await message.channel.send(embed=embed)

    # Open Weather
    if message.content.startswith("$"):
        global info, API_KEY

        try:
            LOCATION = message.content[1:]
            weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={LOCATION}&units=metric&APPID={API_KEY}").json()
            data = info(weather_data)

            embed = discord.Embed(
                    title = LOCATION,
                    description = data,
                    colour = 0x3498DB,
                    timestamp=datetime.datetime.utcnow()
            )
            
            await message.channel.send(embed=embed)
            
        except:
            embed = discord.Embed(
                    title = "Invalid Location.",
                    colour = 0x992D22,
                    timestamp=datetime.datetime.utcnow()
            )
            await message.channel.send(embed=embed)
            
# Runs bot
client.run(bot_token)
