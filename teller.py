#!/usr/bin/python
# coding=utf-8
import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback
import requests
import xml.etree.ElementTree as ET
import noti




def XML_parse():
    url = 'https://api.odcloud.kr/api/15067819/v1/uddi:bab0fa12-d7d7-4e47-975c-e35d424ae165?page=1&perPage=10&returnType=XML'
    service_key = "/ruEDWbFRa8SMf4ev1DPLwU307V7q7mQg9PPlx7euo7NQ+ktMmwxuICWtFUwJN8BKLv+HpKoHipHpOdeVE6qCw=="
    queryParams = {'serviceKey': service_key}
    response = requests.get(url, params=queryParams)

    root = ET.fromstring(response.text)
    results = []
    for item in root.findall('data/item'):
        result = {}
        for col in item.findall('col'):
            name = col.attrib['name']
            value = col.text
            result[name] = value
        results.append(result)
    return results




def replyAptData(user,value):
    print(user, value)
    res_list = noti.getData( value )
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '해당하는 데이터가 없습니다.')

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage( user, row )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    check_list=XML_parse() #확인용 임시 리스트 저장

    text = msg['text']
    args = text.split(' ')
    print(args)
    check=False
    a=''
    for d in check_list:
        #for k,v in d.items():
        if len(args)>1:
            result=' '.join(args)
            print(result)
            if d['TITLE']==result:
                print('{0} 검색'.format(result))
                replyAptData(chat_id, result)
                check = True
        else:
            if d['TITLE']==args[0]:
                print('{0} 검색'.format(args[0]))
                replyAptData(chat_id, args[0])
                check=True
    if not check:
        noti.sendMessage(chat_id, '모르는 명령어입니다.')




today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )

bot = telepot.Bot(noti.TOKEN)
print(bot.getMe())

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)