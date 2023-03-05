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
API_KEY = "Insert Open Weather API Key"


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

    # Help Command
    if message.content.startswith("?help"):
        embed = discord.Embed(
                title="COMMANDS",
                description="Here is the list of commands!",
                colour = 0x3498DB,
                timestamp=datetime.datetime.utcnow()
        )

        embed.add_field(
            name = "Help & Support", 
            value = "?help \n?donate",
            inline = False
        )

        embed.add_field(
            name = "Weather Commands", 
            value = "$London, GB \n$ + city, country initals",
            inline = False
        )

        embed.set_author(name="WEATHER BOT", icon_url="https://media.discordapp.net/attachments/1081590091182510220/1081905211787989003/weather2.png?width=469&height=469")

        await message.channel.send(embed=embed)

    # Donate Command
    if message.content.startswith("?donate"):
        embed = discord.Embed(
            description = "BTC address : bc1q2slgd0du9tfhh7yyjzfa02pnxdjunw20ldhurt \nETH address : 0x67350aB07FBd1115FF7E480AddEf6DA97873879b",
            colour = 0x57F287
        )

        embed.set_author(name = "DONATE", icon_url="https://media.discordapp.net/attachments/1081590091182510220/1081979344978727092/donate.png?width=469&height=469")

        await message.channel.send(embed=embed)

    # Open Weather Command
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

            embed.set_author(name="ERROR", icon_url="https://media.discordapp.net/attachments/1081590091182510220/1081976393899966564/error.jpg?width=469&height=469")

            await message.channel.send(embed=embed)

# Runs bot
client.run(bot_token)
