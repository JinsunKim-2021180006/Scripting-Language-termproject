#!/usr/bin/python
# coding=utf-8
import requests
import xml.etree.ElementTree as ET
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

key = '/ruEDWbFRa8SMf4ev1DPLwU307V7q7mQg9PPlx7euo7NQ+ktMmwxuICWtFUwJN8BKLv+HpKoHipHpOdeVE6qCw=='
TOKEN = '6078174572:AAGdJ1nElVLS1CV_lC19aqfeycFszn387BQ'
MAX_MSG_LENGTH = 300
baseurl = 'https://api.odcloud.kr/api/15067819/v1/uddi:bab0fa12-d7d7-4e47-975c-e35d424ae165?page=1&perPage=10&returnType=XML'
bot = telepot.Bot(TOKEN)


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

def getData(value):
    parsed=XML_parse()
    res_list = []
    for d in parsed:
        for k,v in d.items():
            if v==value:
                temp=d

    name = temp['TITLE']  # 이름
    season = temp['D_SUMMARY']  # 별이 뜨는 계절
    position = temp['POSITION']  # 위치
    engName = temp['SCIENTIFIC_NM']  # 영어이름
    starcount = temp['STAR_COUNT']  # 별자리를 이루는 별 개수
    row='이름: '+name+'\n'+'계절: '+season+'\n'+'위치: '+position+'\n'+'영어 이름: '+engName+'\n'+'별 개수: '+starcount

    if row:
        res_list.append(row.strip())
    return res_list


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print('[',today,']received token :', TOKEN)

    print(bot.getMe())

    run(current_month)
