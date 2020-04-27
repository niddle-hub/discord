import discord
import asyncio
import os
import psycopg2

client = discord.Client()

@client.event
async def on_connect():
    print('Client connect to discord!')

@client.event
async def on_ready():
    for guild in client.guilds:
        print('    Bot ready on <<' + guild.name + '>> server')

@client.event 
async def on_message(message):
    channel = message.channel

    if message.author == client.user:
        return

    if message.content.startswith('!who'):
        await channel.send("итс донт ворк")

    if message.content.startswith('!top'):
        await channel.send("итс донт ворк")

    if message.content.startswith('!help'):
        emb = discord.Embed(title = "Команды бота", colour = 0xffc0cb)
        emb.add_field(name="!help", value="Показывает это сообщение")
        emb.add_field(name="!who", value="отключено")
        emb.add_field(name="!top", value="отключено")
        await channel.send(embed=emb)

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