import discord
import sqlite3
import asyncio
import pytz
import os
from datetime import datetime

client = discord.Client()
db = sqlite3.connect("discord.db")
tz = pytz.timezone('Asia/Yekaterinburg')

@client.event
async def on_connect():
    print('Client connect to discord!')

@client.event
async def on_ready():
    for guild in client.guilds:
        print('    Bot ready on <<' + guild.name + '>> server')
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS `%s` (
            `u_id` INTEGER PRIMARY KEY AUTOINCREMENT, 
            `dis_id` int(20) UNIQUE, 
            `gay_role` boolean DEFAULT 0, 
            `gay_count` int(11) DEFAULT 0 );
            """ % guild.id
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print (e)
        else:
            for member in guild.members:
                if member.bot == False:
                    sql = """INSERT INTO `%s` (dis_id) VALUES (?)""" % guild.id
                    try:
                        cursor.execute(sql, (member.id,))
                        db.commit()
                    except Exception:
                        pass
        finally:
            cursor.close()

@client.event 
async def on_message(message):
    channel = message.channel

    if message.author == client.user:
        return

    if message.content.startswith('!who'):
        cursor = db.cursor()
        sql = """SELECT `dis_id` FROM `%s` WHERE `gay_role` = 1 LIMIT 1""" % message.guild.id
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
        finally:
            cursor.close()

    if message.content.startswith('!top'):
        toplist=[]
        cursor = db.cursor()
        sql = "SELECT `dis_id`, `gay_count` FROM `%s` ORDER BY `gay_count` DESC LIMIT 10" % message.guild.id
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
        finally:
            cursor.close()

    if message.content.startswith('!help'):
        emb = discord.Embed(title = "гейские команды", colour = 0xffc0cb)
        emb.add_field(name="!help", value="Показывает это сообщение")
        emb.add_field(name="!who", value="Показать кто сйечас пидор")
        emb.add_field(name="!top", value="Показать топ 10 пидоров")
        await channel.send(embed=emb)

@client.event
async def on_member_join(member):
    for TextChannel in member.guild.text_channels:
        await TextChannel.send("Приветствуем тебя <@{0}>".format(member.id))
        break

@client.event
async def on_member_remove(member):
    for TextChannel in member.guild.text_channels:
        await TextChannel.send("Попрощаемся с <@{0}>".format(member.id))
        break

async def get_gay():
    await client.wait_until_ready()
    await asyncio.sleep(2)
    timer = datetime(year = 2020, month=12, day=31, hour = 10, minute = 0, second = 0).strftime('%X')
    while not client.is_closed():
        now = datetime.now(tz).strftime('%X')
        if now == timer:
            try:
                cursor = db.cursor()
                for guild in client.guilds:
                    sql = "UPDATE `%s` SET `gay_role` = 0 WHERE `gay_role` = 1" % guild.id
                    cursor.execute(sql)
                    sql = "SELECT `dis_id` FROM `%s` ORDER BY RANDOM() LIMIT 1;" % guild.id
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    sql = "UPDATE `%s` SET `gay_role` = 1 , `gay_count` = `gay_count` + 1 WHERE `dis_id` = %s" % (guild.id, str(result[0]))
                    cursor.execute(sql)
                    db.commit()
                    for TextChannel in guild.text_channels:
                        await TextChannel.send("Пидорас дня => <@" + str(result[0]) + ">")
                        break
            except Exception as e:
                print(e)
            finally:
                await asyncio.sleep(86395)
        await asyncio.sleep(1)

client.bg_task = client.loop.create_task(get_gay())
TOKEN = os.environ.get('BOT_TOKEN')
client.run(str(TOKEN))
db.close()