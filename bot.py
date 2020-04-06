import config
import discord
import pymysql
import asyncio
import os
import schedule
import time

client = discord.Client()

db = pymysql.connect('31.31.196.157', config.LOG, config.PASS, config.DB)

@client.event
async def on_ready():
    print('Bot ready')
    for guild in client.guilds:
        for member in guild.members:
            if member.id != 693871698298142721:
                cursor = db.cursor()
                sql = "INSERT INTO users (dis_id, dis_nick) VALUES (%s, %s)"
                try:
                    cursor.execute(sql, (str(member.id), str(member)))
                    db.commit()
                except Exception as e:
                    print("В запросе возникла ошибка !"+'\n'+str(e))
                    db.rollback()

@client.event 
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!who'):
        channel = message.channel
        cursor = db.cursor()
        sql = "SELECT dis_id FROM users WHERE gay_role = 1 LIMIT 1"
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result == None:
                await channel.send("К сожалению сегодня все натуралы :(")
            else:
                await channel.send("На сегодня пидорас => <@" + str(result[0]) + ">")
        except Exception as e:
            print("Ошибка при выполнении запроса: " + str(e))
            db.rollback()

    if message.content.startswith('!top'):
        toplist=[]
        channel = message.channel
        cursor = db.cursor()
        sql = "SELECT dis_id, gay_count FROM users ORDER BY gay_count DESC LIMIT 10"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                dis_id = row[0]
                gay_count = row[1]
                toplist.append("<@" + str(dis_id) +"> был пидорасом "+ str(gay_count) + " раз\n")

            await channel.send(''.join(toplist))
        except Exception as e:
            print("Ошибка при выполнении запроса: " + str(e))
            db.rollback()

    if message.content.startswith('!help'):
        channel = message.channel
        emb = discord.Embed(title = "гейские команды", colour = 0xffc0cb)
        emb.add_field(name="!help", value="Показывает это сообщение")
        emb.add_field(name="!who", value="Показать кто сйечас пидор")
        emb.add_field(name="!top", value="Показать топ 10 пидоров")
        await channel.send(embed=emb)


@client.event
async def on_member_join(member):
    channel = client.get_channel(config.CHANNEL_ID)
    cursor = db.cursor()
    sql = "INSERT INTO users (dis_id, dis_nick) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (str(member.id), str(member)))
        db.commit()
        await channel.send("Приветствуем тебя <@{0}> на нашем НЕ гетероСЕКСУАЛЬНОМ кАНАЛЕ".format(member.id))
    except Exception as e:
        print(e)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(config.CHANNEL_ID)
    cursor = db.cursor()
    sql = "DELETE FROM users WHERE dis_id = %s OR dis_nick = %s"
    try:
        cursor.execute(sql, (str(member.id), str(member)))
        db.commit()
        await channel.send("Нас покидает <@{0}> ...................... похуй......🕯".format(member.id))
    except Exception as e:
        print(e)

async def get_gay():
    await client.wait_until_ready()
    # await asyncio.sleep(86400)
    channel = client.get_channel(config.CHANNEL_ID)
    while not client.is_closed():
        try:
            cursor = db.cursor()
            sql = "UPDATE users SET gay_role = 0 WHERE gay_role = 1"
            cursor.execute(sql)
            sql = "SELECT dis_id FROM users WHERE dis_id != 693871698298142721 ORDER BY RAND() LIMIT 1;"
            cursor.execute(sql)
            result = cursor.fetchone()
            sql = "UPDATE users SET gay_role = 1 , gay_count = gay_count + 1 WHERE dis_id = %s"
            cursor.execute(sql, str(result[0]))
            db.commit()
            await channel.send("Пидорас дня => <@" + str(result[0]) + ">")
        except Exception as e:
            print(e)

        # await asyncio.sleep(86400) # task runs every N seconds

async def testi():
    print("I'm working...")

schedule.every(10).seconds.do(testi)
# schedule.every().day.at("10:00").do(get_gay)

while True:
    schedule.run_pending()
    time.sleep(1)

# client.bg_task = client.loop.create_task(get_gay())
TOKEN = os.environ.get('BOT_TOKEN')
client.run(str(TOKEN))
db.close()