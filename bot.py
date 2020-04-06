import config
import discord
import asyncio
import os

client = discord.Client()

@client.event
async def on_ready():
    print('Bot ready')

@client.event 
async def on_message(message):
    if message.author == client.user:
        return
    
TOKEN = os.environ.get('BOT_TOKEN')
client.run(str(TOKEN))
