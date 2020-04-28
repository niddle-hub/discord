import discord
import asyncio
import psycopg2
import random
import os

#test

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

    if message.content.startswith('!монетка'):
    	place = ["🔴 Орёл","🔵 Решка"]
    	await channel.send(random.choice(place))

    if message.content.startswith('!who'):
        args = message.content.split()[1:]
        answer = 'Пидоры собрались узнать кто из них самый главный пидор. '
        if len(args) > 0:
            answer = answer + 'Им стал ' + random.choice(args) + '.'
        else:
            answer = answer + 'Но на вечеринку никто не пришел.'
        await channel.send(answer)
		
    if message.content.startswith('!help'):
    	# str(hex(random.randint(0, 0xFFFFFF)))
        emb = discord.Embed(title = "Команды бота", colour = 0x9b59b6)
        emb.add_field(name="!help", value="Показывает это сообщение")
        emb.add_field(name="!монетка", value="подбрасывает монетку")
        emb.add_field(name="!who", value="Выясняет кто главный пидор")
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