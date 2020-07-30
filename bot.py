import discord
import asyncio
import random
import os

client = discord.Client()

@client.event
async def on_connect():
    print('Client connect to discord!')

@client.event
async def on_ready():
    for guild in client.guilds:
        print('Bot ready on <<' + guild.name + '>> server')

@client.event 
async def on_message(message):
    channel = message.channel

    if message.author == client.user:
        return

    if message.content.startswith('!монетка'):
        place = ["🔴 Орёл","🔵 Решка"]
        await channel.send(random.choice(place))

    if message.content.startswith('!help'):
        emb = discord.Embed(title = "Команды бота", colour = 0x9b59b6)
        emb.add_field(name="!help", value="Показывает это сообщение")
        emb.add_field(name="!монетка", value="подбрасывает монетку")
        await channel.send(embed=emb)

@client.event
async def on_voice_state_update(member,before,after):
    if member.voice.channel.id == 737973690255409183:
        new_channel = await member.guild.create_voice_channel(member.name)
        await member.move_to(new_channel)
        def check():
            return len(new_channel.members) == 0
        await client.wait_for('voice_state_update', check=check)
        await new_channel.delete()

@client.event
async def on_member_join(member):
    for TextChannel in member.guild.text_channels:
        await TextChannel.send("К нам зяглянул <@{0}> ...................... заебись......👍".format(member.id))

@client.event
async def on_member_remove(member):
    for TextChannel in member.guild.text_channels:
        await TextChannel.send("Нас покидает <@{0}> ...................... похуй......🕯".format(member.id))

TOKEN = os.environ.get('BOT_TOKEN')
client.run(str(TOKEN))