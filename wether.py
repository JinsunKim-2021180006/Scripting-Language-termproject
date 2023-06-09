import requests
import xml.etree.ElementTree as ET

def lookUpWeather():
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    serviceKey = 'Nt9JLubbJypY+2kCOW3BhPuQjwuYm0o7eHRKSvBxk7aUk/CI9KgBzv06qHctRy26s56jTjqI0kdOKj1gy3oI8Q=='
    type = 'xml'  # 조회하고 싶은 type(json, xml 중 고름)
    baseDate = '20230608'  # 조회하고싶은 날짜
    baseTime = '0500'  # 조회하고싶은 시간
    nx = '60'  # 위도
    ny = '125'  # 경도

    params = {
        'serviceKey': serviceKey,
        'pageNo' : '1',
        'numOfRows' : '1000',
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
        fcstValue = item.find('fcstValue').text

        if category == 'SKY':
            weather = '현재 날씨는 '
            if fcstValue == '1':
                weather += '맑은 상태로'
            elif fcstValue == '2':
                weather += '비가 오는 상태로 '
            elif fcstValue == '3':
                weather += '구름이 많은 상태로 '
            elif fcstValue == '4':
                weather += '흐린 상태로 '

        if category == 'T3H' or category == 'T1H':
            temperature = '기온은 {}℃ 입니다.'.format(fcstValue)

    if weather is not None:
        print(weather)
    if temperature is not None:
        print(temperature)

lookUpWeather()
