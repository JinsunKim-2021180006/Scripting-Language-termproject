import requests
import xml.etree.ElementTree as ET
import gps
import datetime


current_datetime = datetime.datetime.now()
day = current_datetime.strftime("%Y%m%d")
H = current_datetime.strftime("%H")     # 시간
M = current_datetime.strftime("%M")     # 분
Ttime = 0
if int(M) <= 30:
    Ttime = H+"30" 
    M = '00'
else:
    Ttime = str(int(H)+1)+"00"
    M = '30'
time = H+M

if int(Ttime)<1000:
    Ttime = '0'+Ttime

def lookUpWeather():
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    serviceKey = 'Nt9JLubbJypY+2kCOW3BhPuQjwuYm0o7eHRKSvBxk7aUk/CI9KgBzv06qHctRy26s56jTjqI0kdOKj1gy3oI8Q=='
    type = 'xml'  # 조회하고 싶은 type(json, xml 중 고름)
    baseDate = day  # 조회하고싶은 날짜
    baseTime = time[:4]  # 조회하고싶은 시간
    nx = str(int(gps.latitude))  # 위도
    ny = str(int(gps.longitude))  # 경도


    params = {
        'serviceKey': serviceKey,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': type,
        'base_date': baseDate,
        'base_time': baseTime,
        'nx': nx,
        'ny': ny
    }

    response = requests.get(url, params=params)
    xml_data = response.content.decode('utf-8')

    root = ET.fromstring(xml_data)
    items = root.findall('.//item')

    weather = None
    temperature = None

    for item in items:
        category = item.find('category').text
        fcstTime = item.find('fcstTime').text
        fcstValue = item.find('fcstValue').text

        if category == 'SKY':
            if fcstTime == Ttime:
                weather = '현재 날씨는 '
                if fcstValue == '1':
                    weather += '맑은 상태로'
                elif fcstValue == '2':
                    weather += '비가 오는 상태로 '
                elif fcstValue == '3':
                    weather += '구름이 많은 상태로 '
                elif fcstValue == '4':
                    weather += '흐린 상태로 '

                if fcstValue !='1':
                    weather += '별 관측하기 어려울 것 같아요.'

        if category == 'T3H' or category == 'T1H':
            if fcstTime == Ttime:
                temperature = '기온은 {}℃ 입니다.'.format(fcstValue)

    result='현재 기상 정보가 없습니다.'
    if weather is not None and temperature is not None:
        result=weather+'\n'+temperature

    return result

if __name__ == "__main__":
    print(lookUpWeather())



