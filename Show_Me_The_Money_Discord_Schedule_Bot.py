import discord, asyncio, os
from discord.ext import commands, tasks
import datetime as dt
from datetime import date
import sqlite3
import shutil
import re
import pymysql
import time


bot = commands.Bot(command_prefix='~')

data={}
data['when'] = 898830780682350622
data['bal_nor'] = 898830880058015754
data['bal_hard'] = 898830885518991371
data['bia_nor'] = 898830919606099988
data['bia_hard'] = 898830924240801802
data['cook_nor'] = 898830931891195974
data['argo'] = 898830944860004362
data['arv_nor_1_2'] = 898830949540843541
arv_hard = 0

@bot.event
async def on_ready():
    data_db = pymysql.connect(
        user=os.environ['USER_NAME'],
        passwd=os.environ['USER_PASSWD'],
        host=os.environ['USER_HOST'],
        db=os.environ['USER_DB_NAME'],
        autocommit=True
    )
    curs = data_db.cursor()

    curs.execute('CREATE TABLE IF NOT EXISTS NOW_RADE (author text, bal_nor integer default 0, bal_hard integer default 0,\
    bia_nor integer default 0, bia_hard integer default 0, cook_nor integer default 0, argo integer default 0, \
        arv_nor_1_2 integer default 0)')

    curs.execute('CREATE TABLE IF NOT EXISTS WED (author text, bal_nor integer default 0, bal_hard integer default 0,\
    bia_nor integer default 0, bia_hard integer default 0, cook_nor integer default 0, argo integer default 0, \
        arv_nor_1_2 integer default 0)')

    game = discord.Game("GIVE ME THE MONEY")
    await bot.change_presence(status=discord.Status.online, activity=game)  
    print("Start Bot\n")
        
@tasks.loop(seconds=10)
async def chk_date():
    ch = bot.get_channel(898561134783787028)
    
    NOW_RADE = dt.datetime.now()+dt.timedelta(hours=7)
    print(NOW_RADE.weekday())
    print(NOW_RADE.hour)
    if NOW_RADE.weekday() == 2 and NOW_RADE.hour > 6:
        st = dt.datetime(2021,10,6,10,0,0)
        ed = dt.datetime(2021,10,13,6,0,0)
        NOW_RADE = dt.datetime.now()
        while ed < NOW_RADE:
            st = st + dt.timedelta(days=7)
            ed = ed + dt.timedelta(days=7)
        text = ' `📢 {}월 / {}일 ~  {}월 / {}일 주간 레이드 ` '.format(st.month,st.day,ed.month,ed.day)
        embed = discord.Embed(title = text,color = 0xFF0000)
        message = await ch.fetch_message(data['when'])
        await message.edit(embed=embed)

        data_db = pymysql.connect(
            user=os.environ['USER_NAME'],
            passwd=os.environ['USER_PASSWD'],
            host=os.environ['USER_HOST'],
            db=os.environ['USER_DB_NAME'],
            autocommit=True
        )
        curs = data_db.cursor()
        curs.execute('DROP TABLE IF EXISTS `NOW_RADE`')
        curs.execute('Create Table `NOW_RADE` (SELECT * FROM `WED`)')
        bs = ""
        mes=['발노','발하','비노','비하','쿠크','알고','아브']
        for ms in mes:
            if ms in '발탄' or ms in '발':
                if '노말' in ms or '노' in ms:
                    bs="bal_nor"
                    embed = discord.Embed(title = ' `🐃 발탄 노말 🐃` ' ,color = 0xFF0000)


                elif '하드' in ms or '하' in ms:
                    bs='bal_hard'
                    embed = discord.Embed(title = ' `🐃 발탄 하드 🐃` ' ,color = 0xFF0000)


            elif  '비아키스' in ms or '비아' in ms or '비' in ms:
                if '노말' in ms or '노' in ms:
                    bs='bia_nor'
                    embed = discord.Embed(title =' ` 💃 비아 노말 💃 ` ',color = 0xFF0000)


                elif '하드' in ms or '하' in ms:
                    bs='bia_hard'
                    embed = discord.Embed(title =' ` 💃 비아 하드 💃 ` ',color = 0xFF0000)


            elif '쿠크' in ms:
                bs='cook_nor'
                embed = discord.Embed(title =' ` 🎲 쿠크 노말 🎲 ` ',color = 0xFF0000)


            elif '아르고스' in ms or '알고' in ms:
                bs='argo'
                embed = discord.Embed(title =' ` 🐐 아르고스 🐐 ` ',color = 0xFF0000)

            elif '아브렐슈드' in ms or '아브' in ms:
                bs='arv_nor_1_2'
                embed = discord.Embed(title =' ` 👾 아브렐슈드 1 ~ 2페 👾 ` ',color = 0xFF0000)

            query='SELECT AUTHOR, {} FROM WED WHERE {} > 0'.format(bs,bs)
            curs.execute(query)
            for row in curs.fetchall():
                embed.add_field(name=row[0],value=row[1],inline=True)
            message = await ch.fetch_message(data[bs])
            await message.edit(embed=embed)
            
    time.sleep(5)

    return
        
@bot.event
async def on_message(message):
    if message.author == bot.user or len(message.content) == 0:
        return
    
    if message.content[0]!='~':
        return
    
    if message.content == '~hello':
        await message.channel.send(f'{message.author.mention}님 저리가세요!')
        return
    
    if message.content == '~bye':
        await message.channel.send(f'{message.author.mention}님 게임좀 그만하세요!')
        return

    await asyncio.sleep(0.3)
    await message.delete()
    await asyncio.sleep(0.3)
    
    ch = bot.get_channel(898561134783787028)
    bosses = ['발', '발탄', '비', '비아키스', '비아', '쿠크세이튼', '쿠크', '아르고스', '알고', '아브렐슈드', '아브']

    if message.content == '~한남재훈':
        await message.channel.send(f'{message.author.mention}님 께서 서버를 공격하고 계십니다!')

        data_db = pymysql.connect(
            user=os.environ['USER_NAME'],
            passwd=os.environ['USER_PASSWD'],
            host=os.environ['USER_HOST'],
            db=os.environ['USER_DB_NAME'],
            autocommit=True
        )
        curs=data_db.cursor()
        
        curs.execute('DROP TABLE IF EXISTS `NOW_RADE`')
        curs.execute('DROP TABLE IF EXISTS `WED`')

        curs.execute('CREATE TABLE IF NOT EXISTS NOW_RADE (author text, bal_nor integer default 0, bal_hard integer default 0,\
        bia_nor integer default 0, bia_hard integer default 0, cook_nor integer default 0, argo integer default 0, \
        arv_nor_1_2 integer default 0)')

        curs.execute('CREATE TABLE IF NOT EXISTS WED (author text, bal_nor integer default 0, bal_hard integer default 0,\
        bia_nor integer default 0, bia_hard integer default 0, cook_nor integer default 0, argo integer default 0, \
            arv_nor_1_2 integer default 0)')

        mes=['발노','발하','비노','비하','쿠크','알고','아브']
        bs=""
        for ms in mes:
            if '발탄' in ms or '발' in ms:
                if '노말' in ms or '노' in ms:
                    bs="bal_nor"
                    embed = discord.Embed(title = ' `🐃 발탄 노말 🐃` ' ,color = 0xFF0000)


                elif '하드' in ms or '하' in ms:
                    bs='bal_hard'
                    embed = discord.Embed(title = ' `🐃 발탄 하드 🐃` ' ,color = 0xFF0000)


            elif  '비아키스' in ms or '비아' in ms or '비' in ms:
                if '노말' in ms or '노' in ms:
                    bs='bia_nor'
                    embed = discord.Embed(title =' ` 💃 비아 노말 💃 ` ',color = 0xFF0000)


                elif '하드' in ms or '하' in ms:
                    bs='bia_hard'
                    embed = discord.Embed(title =' ` 💃 비아 하드 💃 ` ',color = 0xFF0000)


            elif '쿠크' in ms:
                bs='cook_nor'
                embed = discord.Embed(title =' ` 🎲 쿠크 노말 🎲 ` ',color = 0xFF0000)


            elif '아르고스' in ms or '알고' in ms:
                bs='argo'
                embed = discord.Embed(title =' ` 🐐 아르고스 🐐 ` ',color = 0xFF0000)

            elif '아브렐슈드' in ms or '아브' in ms:
                bs='arv_nor_1_2'
                embed = discord.Embed(title =' ` 👾 아브렐슈드 1 ~ 2페 👾 ` ',color = 0xFF0000)

            print(bs)
            message = await ch.fetch_message(data[bs])
            await message.edit(embed=embed)

        return
    
    if message.content == '~초기화':
        await message.channel.send(f'{message.author.mention}님 께서 서버를 해킹하고 계십니다')

        data_db = pymysql.connect(
            user=os.environ['USER_NAME'],
            passwd=os.environ['USER_PASSWD'],
            host=os.environ['USER_HOST'],
            db=os.environ['USER_DB_NAME'],
            autocommit=True
        )
        curs=data_db.cursor()
        curs.execute('DROP TABLE IF EXISTS `NOW_RADE`')
        curs.execute('Create Table `NOW_RADE` (SELECT * FROM `WED`)')
        bs = ""
        mes=['발노','발하','비노','비하','쿠크','알고','아브']
        for ms in mes:
            if '발탄' in ms or '발' in ms:
                if '노말' in ms or '노' in ms:
                    bs="bal_nor"
                    embed = discord.Embed(title = ' `🐃 발탄 노말 🐃` ' ,color = 0xFF0000)


                elif '하드' in ms or '하' in ms:
                    bs='bal_hard'
                    embed = discord.Embed(title = ' `🐃 발탄 하드 🐃` ' ,color = 0xFF0000)


            elif  '비아키스' in ms or '비아' in ms or '비' in ms:
                if '노말' in ms or '노' in ms:
                    bs='bia_nor'
                    embed = discord.Embed(title =' ` 💃 비아 노말 💃 ` ',color = 0xFF0000)


                elif '하드' in ms or '하' in ms:
                    bs='bia_hard'
                    embed = discord.Embed(title =' ` 💃 비아 하드 💃 ` ',color = 0xFF0000)


            elif '쿠크' in ms:
                bs='cook_nor'
                embed = discord.Embed(title =' ` 🎲 쿠크 노말 🎲 ` ',color = 0xFF0000)


            elif '아르고스' in ms or '알고' in ms:
                bs='argo'
                embed = discord.Embed(title =' ` 🐐 아르고스 🐐 ` ',color = 0xFF0000)

            elif '아브렐슈드' in ms or '아브' in ms:
                bs='arv_nor_1_2'
                embed = discord.Embed(title =' ` 👾 아브렐슈드 1 ~ 2페 👾 ` ',color = 0xFF0000)


            query='SELECT AUTHOR, {} FROM `WED` WHERE {} > 0'.format(bs,bs)
            curs.execute(query)
            for row in curs.fetchall():
                embed.add_field(name=row[0],value=row[1],inline=True)
            message = await ch.fetch_message(data[bs])
            await message.edit(embed=embed)
            
        return
    
    if '완료' in message.content or '완' in message.content:
        bs = ""
        for boss in bosses:
            if boss in message.content:   
                if boss == '발탄' or boss == '발':
                    if '노말' in message.content or '노' in message.content:
                        bs="bal_nor"
                        embed = discord.Embed(title = ' `🐃 발탄 노말 🐃` ' ,color = 0xFF0000)


                    elif '하드' in message.content or '하' in message.content:
                        bs='bal_hard'
                        embed = discord.Embed(title = ' `🐃 발탄 하드 🐃` ' ,color = 0xFF0000)


                elif boss == '비아키스' or boss == '비아' or boss == '비':
                    if '노말' in message.content or '노' in message.content:
                        bs='bia_nor'
                        embed = discord.Embed(title =' ` 💃 비아 노말 💃 ` ',color = 0xFF0000)


                    elif '하드' in message.content or '하' in message.content:
                        bs='bia_hard'
                        embed = discord.Embed(title =' ` 💃 비아 하드 💃 ` ',color = 0xFF0000)


                elif boss == '쿠크세이튼' or boss == '쿠크':
                    bs='cook_nor'
                    embed = discord.Embed(title =' ` 🎲 쿠크 노말 🎲 ` ',color = 0xFF0000)


                elif boss == '아르고스' or boss == '알고':
                    bs='argo'
                    embed = discord.Embed(title =' ` 🐐 아르고스 🐐 ` ',color = 0xFF0000)

                elif boss == '아브렐슈드' or boss == '아브':
                    bs='arv_nor_1_2'
                    embed = discord.Embed(title =' ` 👾 아브렐슈드 1 ~ 2페 👾 ` ',color = 0xFF0000)

        if bs != "":
            string = message.content
            try:
                num = int(re.sub(r'[^0-9]', '', string))
            except:
                num = 1
            data_db = pymysql.connect(
                user=os.environ['USER_NAME'],
                passwd=os.environ['USER_PASSWD'],
                host=os.environ['USER_HOST'],
                db=os.environ['USER_DB_NAME'],
                autocommit=True
            )
            curs=data_db.cursor()
            query = 'SELECT EXISTS(SELECT AUTHOR FROM `NOW_RADE` WHERE `AUTHOR` = \'{}\')'.format(str(message.author))
            curs.execute(query)

            a=curs.fetchone()[0]
            if a == 1:
                query = 'SELECT {} FROM `NOW_RADE` WHERE AUTHOR = \'{}\''.format(bs,str(message.author))
                curs.execute(query)
                every_num = curs.fetchone()[0]
                print(every_num)
                num = int(every_num)-num
                if num < 0:
                    num = 0
                query='UPDATE `NOW_RADE` SET {} = {} WHERE `AUTHOR` = \'{}\''.format(bs,num,str(message.author))
                curs.execute(query)
            else:
                await message.channel.send(f'{message.author.mention}님 완료하실 캐릭터가 없습니다!')
                return


            query='SELECT AUTHOR, {} FROM NOW_RADE WHERE {} > 0'.format(bs,bs)
            curs.execute(query)
            for row in curs.fetchall():
                embed.add_field(name=row[0],value=row[1],inline=True)
            message = await ch.fetch_message(data[bs])
            await message.edit(embed=embed)

            return
    
    if '초기' in message.content:
        bs = ""
        for boss in bosses:
            if boss in message.content:   
                if boss == '발탄' or boss == '발':
                    if '노말' in message.content or '노' in message.content:
                        bs="bal_nor"
                        embed = discord.Embed(title = ' `🐃 발탄 노말 🐃` ' ,color = 0xFF0000)


                    elif '하드' in message.content or '하' in message.content:
                        bs='bal_hard'
                        embed = discord.Embed(title = ' `🐃 발탄 하드 🐃` ' ,color = 0xFF0000)


                elif boss == '비아키스' or boss == '비아' or boss == '비':
                    if '노말' in message.content or '노' in message.content:
                        bs='bia_nor'
                        embed = discord.Embed(title =' ` 💃 비아 노말 💃 ` ',color = 0xFF0000)


                    elif '하드' in message.content or '하' in message.content:
                        bs='bia_hard'
                        embed = discord.Embed(title =' ` 💃 비아 하드 💃 ` ',color = 0xFF0000)


                elif boss == '쿠크세이튼' or boss == '쿠크':
                    bs='cook_nor'
                    embed = discord.Embed(title =' ` 🎲 쿠크 노말 🎲 ` ',color = 0xFF0000)


                elif boss == '아르고스' or boss == '알고':
                    bs='argo'
                    embed = discord.Embed(title =' ` 🐐 아르고스 🐐 ` ',color = 0xFF0000)

                elif boss == '아브렐슈드' or boss == '아브':
                    bs='arv_nor_1_2'
                    embed = discord.Embed(title =' ` 👾 아브렐슈드 1 ~ 2페 👾 ` ',color = 0xFF0000)
        if bs != "":                
            string = message.content
            try:
                num = int(re.sub(r'[^0-9]', '', string))
            except:
                num=1

            data_db = pymysql.connect(
                user=os.environ['USER_NAME'],
                passwd=os.environ['USER_PASSWD'],
                host=os.environ['USER_HOST'],
                db=os.environ['USER_DB_NAME'],
                autocommit=True
            )
            curs=data_db.cursor()
            query = 'SELECT EXISTS(SELECT AUTHOR FROM `WED` WHERE `AUTHOR` = \'{}\' ) '.format(str(message.author))
            curs.execute(query)
            a=curs.fetchone()[0]
            if a == 1:
                query='UPDATE `WED` SET {} = \'{}\' WHERE AUTHOR = \'{}\''.format(bs,num,str(message.author))
                curs.execute(query)
            else:
                query='INSERT INTO `WED`(AUTHOR, {}) VALUES ( \'{}\' , {} ) '.format(bs,str(message.author),num)
                curs.execute(query)

            query = 'SELECT EXISTS(SELECT AUTHOR FROM `NOW_RADE` WHERE `AUTHOR` = \'{}\')'.format(str(message.author))
            curs.execute(query)
            a=curs.fetchone()[0]
            if a == 1:
                query='UPDATE `NOW_RADE` SET {} = \'{}\' WHERE AUTHOR = \'{}\''.format(bs,num,str(message.author))
                curs.execute(query)
            else:
                query='INSERT INTO `NOW_RADE` ( AUTHOR, {} ) VALUES ( \'{}\' , {} )'.format(bs,str(message.author),num)
                curs.execute(query)


            query='SELECT AUTHOR, {} FROM `NOW_RADE` WHERE {} > 0'.format(bs,bs)
            curs.execute(query)
            for row in curs.fetchall():
                embed.add_field(name=row[0],value=row[1],inline=True)
            message = await ch.fetch_message(data[bs])
            await message.edit(embed=embed)
            
            return
    
    if message.content == '~날짜':
        st = dt.datetime(2021,10,6,10,0,0)
        ed = dt.datetime(2021,10,13,6,0,0)
        NOW_RADE = dt.datetime.now()+dt.timedelta(hours=7)
        print(NOW_RADE)
        while ed < NOW_RADE:
            st = st + dt.timedelta(days=7)
            ed = ed + dt.timedelta(days=7)
        text = ' `📢 {}월 / {}일 ~  {}월 / {}일 주간 레이드 ` '.format(st.month,st.day,ed.month,ed.day)
        embed = discord.Embed(title = text,color = 0xFF0000)
        message = await ch.fetch_message(data['when'])
        await message.edit(embed=embed)
        return
    
    
    
    print(message.content)
    bs = ""
    for boss in bosses:
        if boss in message.content:   
            if boss == '발탄' or boss == '발':
                if '노말' in message.content or '노' in message.content:
                    bs="bal_nor"
                    embed = discord.Embed(title = ' `🐃 발탄 노말 🐃` ' ,color = 0xFF0000)
                    
                
                elif '하드' in message.content or '하' in message.content:
                    bs='bal_hard'
                    embed = discord.Embed(title = ' `🐃 발탄 하드 🐃` ' ,color = 0xFF0000)

                
            elif boss == '비아키스' or boss == '비아' or boss == '비':
                if '노말' in message.content or '노' in message.content:
                    bs='bia_nor'
                    embed = discord.Embed(title =' ` 💃 비아 노말 💃 ` ',color = 0xFF0000)

                
                elif '하드' in message.content or '하' in message.content:
                    bs='bia_hard'
                    embed = discord.Embed(title =' ` 💃 비아 하드 💃 ` ',color = 0xFF0000)

                
            elif boss == '쿠크세이튼' or boss == '쿠크':
                bs='cook_nor'
                embed = discord.Embed(title =' ` 🎲 쿠크 노말 🎲 ` ',color = 0xFF0000)

                
            elif boss == '아르고스' or boss == '알고':
                bs='argo'
                embed = discord.Embed(title =' ` 🐐 아르고스 🐐 ` ',color = 0xFF0000)
                
            elif boss == '아브렐슈드' or boss == '아브':
                bs='arv_nor_1_2'
                embed = discord.Embed(title =' ` 👾 아브렐슈드 1 ~ 2페 👾 ` ',color = 0xFF0000)

    if bs != "":
        string = message.content
        try:
            num = int(re.sub(r'[^0-9]', '', string))
        except:
            num=1


        data_db = pymysql.connect(
            user=os.environ['USER_NAME'],
            passwd=os.environ['USER_PASSWD'],
            host=os.environ['USER_HOST'],
            db=os.environ['USER_DB_NAME'],
            autocommit=True
        )
        curs=data_db.cursor()
        query = 'SELECT EXISTS ( SELECT AUTHOR FROM `NOW_RADE` WHERE `AUTHOR` = \'{}\' )'.format(str(message.author))
        curs.execute(query)
        a=curs.fetchone()[0]
        if a == 1:
            query='UPDATE `NOW_RADE` SET {} = \'{}\' WHERE AUTHOR = \'{}\''.format(bs,num,str(message.author))
            curs.execute(query)
        else:
            query='INSERT INTO `NOW_RADE`(AUTHOR, {}) VALUES (\'{}\' , {})'.format(bs,str(message.author),num)
            curs.execute(query)


        query='SELECT AUTHOR, {} FROM NOW_RADE WHERE {} > 0'.format(bs,bs)
        curs.execute(query)
        for row in curs.fetchall():
            embed.add_field(name=row[0],value=row[1],inline=True)
        message = await ch.fetch_message(data[bs])
        await message.edit(embed=embed)

        return        

        
    else:
        await message.channel.send("초기, 완료 | 발노,발하 등등 | 0~9 숫자없으면 자동으로 1")
        await message.channel.send("~ | 발탄, 비아키스, 비아, 쿠크세이튼, 쿠크, 아르고스, 알고, 아브렐슈드, 아브 | 노말, 하드 | [1~9]")
        return
    
if __name__ == "__main__":
    #token = open('D:/옮길거/공부/python/디코봇/Token.txt',"r",encoding="utf-8").read()
    #bot.run(token)
    bot.run(os.environ['TOKEN'])