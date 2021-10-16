import discord, asyncio, os
from discord.ext import commands, tasks
import datetime as dt
from datetime import date
import sqlite3
import shutil
import re
import pymysql


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

data_db = pymysql.connect(
    user=os.environ[USER_NAME],
    passwd=os.environ[USER_PASSWD],
    host=os.environ[USER_HOST],
    db=os.environ[USER_DB_NAME],
    autocommit=True
)

@bot.event
async def on_ready():
    curs = data_db.cursor()

    curs.execute('CREATE TABLE IF NOT EXISTS NOW (author text, bal_nor integer default 0, bal_hard integer default 0,\
    bia_nor integer default 0, bia_hard integer default 0, cook_nor integer default 0, argo integer default 0, \
        arv_nor_1_2 integer default 0)')

    curs.execute('CREATE TABLE IF NOT EXISTS INIT (author text, bal_nor integer default 0, bal_hard integer default 0,\
    bia_nor integer default 0, bia_hard integer default 0, cook_nor integer default 0, argo integer default 0, \
        arv_nor_1_2 integer default 0)')

    game = discord.Game("GIVE ME THE MONEY")
    await bot.change_presence(status=discord.Status.online, activity=game)  
    print("Start Bot\n")
        
@tasks.loop(hours=1.0)
async def chk_date():
    ch = bot.get_channel(898561134783787028)
    now = dt.datetime.now()
    if now.weekday() == 2 and now.hour < 10 and now.hour > 6:
        curs = data_db.cursor()
        curs.execute('Create Tabel NOW LIKE INIT')
        bs = ""
        mes=['발노','발하','비노','비하','쿠크','알고','아브']
        for ms in mes:
            if ms == '발탄' or ms == '발':
                if '노말' in ms or '노' in ms:
                    bs="bal_nor"
                    embed = discord.Embed(title = ' `🐃 발탄 노말 🐃` ' ,color = 0xFF0000)


                elif '하드' in ms or '하' in ms:
                    bs='bal_hard'
                    embed = discord.Embed(title = ' `🐃 발탄 하드 🐃` ' ,color = 0xFF0000)


            elif ms == '비아키스' or ms == '비아' or ms == '비':
                if '노말' in ms or '노' in ms:
                    bs='bia_nor'
                    embed = discord.Embed(title =' ` 💃 비아 노말 💃 ` ',color = 0xFF0000)


                elif '하드' in ms or '하' in ms:
                    bs='bia_hard'
                    embed = discord.Embed(title =' ` 💃 비아 하드 💃 ` ',color = 0xFF0000)


            elif ms == '쿠크':
                bs='cook_nor'
                embed = discord.Embed(title =' ` 🎲 쿠크 노말 🎲 ` ',color = 0xFF0000)


            elif ms == '아르고스' or ms == '알고':
                bs='argo'
                embed = discord.Embed(title =' ` 🐐 아르고스 🐐 ` ',color = 0xFF0000)

            elif ms == '아브렐슈드' or ms == '아브':
                bs='arv_nor_1_2'
                embed = discord.Embed(title =' ` 👾 아브렐슈드 1 ~ 2페 👾 ` ',color = 0xFF0000)
                

            query='SELECT AUTHOR, {} FROM INIT WHERE {} > 0'.format(bs,bs)
            curs.execute(query)
            for row in curs.fetchall():
                embed.add_field(name=row[0],value=row[1],inline=True)
            message = await ch.fetch_message(data[bs])
            await message.edit(embed=embed)
            
    

    return
        
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content[0]!='~':
        return
    
    if message.content == '~hello':
        await message.channel.send(f'{message.author.mention}님 저리가세요!')
        return
    
    if message.content == '~bye':
        await message.channel.send(f'{message.author.mention}님 게임좀 그만하세요!')
        return
    await message.delete()
    
    ch = bot.get_channel(898561134783787028)
    bosses = ['발', '발탄', '비', '비아키스', '비아', '쿠크세이튼', '쿠크', '아르고스', '알고', '아브렐슈드', '아브']
    
    if message.content == '~초기화':
        curs=data_db.cursor()
        curs.execute('Create Tabel NOW LIKE INIT')
        bs = ""
        mes=['발노','발하','비노','비하','쿠크','알고','아브']
        for ms in mes:
            if ms == '발탄' or ms == '발':
                if '노말' in ms or '노' in ms:
                    bs="bal_nor"
                    embed = discord.Embed(title = ' `🐃 발탄 노말 🐃` ' ,color = 0xFF0000)


                elif '하드' in ms or '하' in ms:
                    bs='bal_hard'
                    embed = discord.Embed(title = ' `🐃 발탄 하드 🐃` ' ,color = 0xFF0000)


            elif ms == '비아키스' or ms == '비아' or ms == '비':
                if '노말' in ms or '노' in ms:
                    bs='bia_nor'
                    embed = discord.Embed(title =' ` 💃 비아 노말 💃 ` ',color = 0xFF0000)


                elif '하드' in ms or '하' in ms:
                    bs='bia_hard'
                    embed = discord.Embed(title =' ` 💃 비아 하드 💃 ` ',color = 0xFF0000)


            elif ms == '쿠크':
                bs='cook_nor'
                embed = discord.Embed(title =' ` 🎲 쿠크 노말 🎲 ` ',color = 0xFF0000)


            elif ms == '아르고스' or ms == '알고':
                bs='argo'
                embed = discord.Embed(title =' ` 🐐 아르고스 🐐 ` ',color = 0xFF0000)

            elif ms == '아브렐슈드' or ms == '아브':
                bs='arv_nor_1_2'
                embed = discord.Embed(title =' ` 👾 아브렐슈드 1 ~ 2페 👾 ` ',color = 0xFF0000)


            query='SELECT AUTHOR, {} FROM INIT WHERE {} > 0'.format(bs,bs)
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
            num = int(re.sub(r'[^0-9]', '', string))
            if num == 0:
                num = 1

            curs = data_db.cursor()


            curs.execute('SELECT EXISTS(SELECT AUTHOR FROM NOW WHERE AUTHOR=?)',(str(message.author),))
            a=curs.fetchone()[0]
            if a == 1:
                query = 'SELECT {} FROM NOW WHERE AUTHOR = \'{}\''.format(bs,str(message.author))
                num = int(curs.fetchone()[0])-num
                if num < 0:
                    num = 0
                query='UPDATE `NOW` SET {}= ? WHERE AUTHOR = ?'.format(bs)
                curs.execute(query,(num,str(message.author)))
            else:
                await message.channel.send(f'{message.author.mention}님 완료하실 캐릭터가 없습니다!')
                return


            query='SELECT AUTHOR, {} FROM NOW WHERE {} > 0'.format(bs,bs)
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
            num = int(re.sub(r'[^0-9]', '', string))
            if num == 0:
                num = 1

            curs = data_db.cursor()

            curs=data_db.cursor()
            query = 'SELECT EXISTS(SELECT AUTHOR FROM `INIT` WHERE AUTHOR=\'{}\')'.format(str(message.author))
            curs.execute(query)
            a=curs.fetchone()[0]
            if a == 1:
                query='UPDATE `INIT` SET {} = \'{}\' WHERE AUTHOR = \'{}\''.format(bs,num,str(message.author))
                curs.execute(query)
            else:
                query='INSERT INTO `INIT`(AUTHOR, {}) VALUES (\'{}\',{})'.format(bs,str(message.author),num)
                curs.execute(query)

            curs=data_db.cursor()
            query = 'SELECT EXISTS(SELECT AUTHOR FROM `NOW` WHERE AUTHOR=\'{}\')'.format(str(message.author))
            curs.execute(query)
            a=curs.fetchone()[0]
            if a == 1:
                query='UPDATE `NOW` SET {} = \'{}\' WHERE AUTHOR = \'{}\''.format(bs,num,str(message.author))
                curs.execute(query)
            else:
                query='INSERT INTO `NOW`(AUTHOR, {}) VALUES (\'{}\',{})'.format(bs,str(message.author),num)
                curs.execute(query)


            query='SELECT AUTHOR, {} FROM NOW WHERE {} > 0'.format(bs,bs)
            curs.execute(query)
            for row in curs.fetchall():
                embed.add_field(name=row[0],value=row[1],inline=True)
            message = await ch.fetch_message(data[bs])
            await message.edit(embed=embed)
            
            return
    
    if message.content == '~날짜':
        st = dt.datetime(2021,10,6,10,0,0)
        ed = dt.datetime(2021,10,13,6,0,0)
        now = dt.datetime.now()
        while ed < now:
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
        num = int(re.sub(r'[^0-9]', '', string))
        if num == 0:
            num = 1

        curs=data_db.cursor()
        query = 'SELECT EXISTS(SELECT AUTHOR FROM `NOW` WHERE AUTHOR=\'{}\')'.format(str(message.author))
        curs.execute(query)
        a=curs.fetchone()[0]
        if a == 1:
            query='UPDATE `NOW` SET {} = \'{}\' WHERE AUTHOR = \'{}\''.format(bs,num,str(message.author))
            curs.execute(query)
        else:
            query='INSERT INTO `NOW`(AUTHOR, {}) VALUES (\'{}\',{})'.format(bs,str(message.author),num)
            curs.execute(query)


        query='SELECT AUTHOR, {} FROM NOW WHERE {} > 0'.format(bs,bs)
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