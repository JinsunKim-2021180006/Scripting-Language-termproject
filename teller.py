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
from tkinter import *
from telepot.loop import MessageLoop


bot = telepot.Bot(noti.TOKEN)
def tel_search(input_text):
    TOKEN = '6078174572:AAGdJ1nElVLS1CV_lC19aqfeycFszn387BQ'
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    res_list = noti.getData(input_text)
    msg = ''
    for r in res_list:
        print(str(datetime.now()).split('.')[0], r)
        if len(r + msg) + 1 > noti.MAX_MSG_LENGTH:
            noti.sendMessage(6100292453, msg)
            msg = r + '\n'
        else:
            msg += r + '\n'
        if msg:
            noti.sendMessage(6100292453, msg)
        else:
            noti.sendMessage(6100292453, '해당하는 데이터가 없습니다.')
    #bot.sendMessage(6100292453, noti.getData(input_text))  # 텔레그램으로 메시지 발송
    """
    params = {
        'chat_id': '6100292453',
        'text': input_text
    }
    response = requests.post(url, params)
"""

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

def window():
    run()
    telwindow = Toplevel()
    telwindow.title("텔레그램")
    telwindow.geometry('200x80')
    telwindow.config(bg="#231B61")

    label = Label(telwindow, text="별자리 검색", font=("돋음", 10), background="#231B61", foreground="white")
    label.grid(column=0, row=0)

    input= Entry(telwindow, width=30)
    input.grid(column=0, row=2)

    button = Button(telwindow, text="확인", command=lambda: tel_search(input.get()))
    button.grid(column=0, row=3)


def run():
    MessageLoop(bot, handle).run_as_thread()


def main(input_text):
    today = date.today()
    current_month = today.strftime('%Y%m')


    print( '[',today,']received token :', noti.TOKEN )

    bot = telepot.Bot(noti.TOKEN)
    print(bot.getMe())

    bot.message_loop(handle)

    print('Listening...')

    while 1:
      time.sleep(10)


"""
title 검색
처녀자리	
거문고자리
독수리자리
뱀자리 / 뱀주인자리
페가수스자리
물병자리 / 남쪽물고기자리
도마뱀자리 / 조랑말자리
쌍둥이자리	
오리온자리	
케페우스자리
"""