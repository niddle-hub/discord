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
    try:
        if after.channel.id == 737973690255409183:
            new_channel = await member.guild.create_voice_channel(member.name, category = member.guild.categories[2])
            await member.move_to(new_channel)
            def check(a,b,c):
                return len(new_channel.members) == 0
            await client.wait_for('voice_state_update', check=check)
            await new_channel.delete()
        elif after.channel.id == 738715723442159677:
            new_channel = await member.guild.create_voice_channel(name = "Частный канал {0}".format(member.name), category = member.guild.categories[3], user_limit = 2)
            await member.move_to(new_channel)
            def check(a,b,c):
                return len(new_channel.members) == 0
            await client.wait_for('voice_state_update', check=check)
            await new_channel.delete()
        elif after.channel.id == 738715774444896297:
            new_channel = await member.guild.create_voice_channel(name = "Частный канал {0}".format(member.name), category = member.guild.categories[3], user_limit = 3)
            await member.move_to(new_channel)
            def check(a,b,c):
                return len(new_channel.members) == 0
            await client.wait_for('voice_state_update', check=check)
            await new_channel.delete()
        elif after.channel.id == 738715823887220768:
            new_channel = await member.guild.create_voice_channel(name = "Частный канал {0}".format(member.name), category = member.guild.categories[3], user_limit = 4)
            await member.move_to(new_channel)
            def check(a,b,c):
                return len(new_channel.members) == 0
            await client.wait_for('voice_state_update', check=check)
            await new_channel.delete()
        elif after.channel.id == 738715851691130931:
            new_channel = await member.guild.create_voice_channel(name = "Частный канал {0}".format(member.name), category = member.guild.categories[3], user_limit = 5)
            await member.move_to(new_channel)
            def check(a,b,c):
                return len(new_channel.members) == 0
            await client.wait_for('voice_state_update', check=check)
            await new_channel.delete()
        else:
            pass
    except:
        pass

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