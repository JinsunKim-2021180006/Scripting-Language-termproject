import requests
import xml.etree.ElementTree as ET
import tkinter as tk
#pip install gpsd-py3
import gpsd
from opensite import *

def get_current_location():
    gpsd.connect()

    # gpsd에서 위치 데이터 가져오기
    packet = gpsd.get_current()

    if packet.mode >= 2:
        # 유효한 위치 데이터인 경우
        latitude = packet.lat #위도
        longitude = packet.lon #경도

        return latitude, longitude
    else:
        # 유효한 위치 데이터가 아닌 경우
        return None


def open_new_window():
    search_star = tk.Toplevel(window)  # 새로운 창을 생성합니다
    search_star.title("별자리 검색하기")
    search_star.geometry('600x500')

    label = tk.Label(search_star, text="별자리명을 입력하세요",font=("Helvetica", 10))
    label.pack()

    entry = tk.Entry(search_star, width=45)
    entry.pack()

    constellation_name = entry.get()

    info=xml_parse() #딕셔너리 반환

    #info_label = tk.Label(search_star, text="")

    label_text = tk.StringVar()
    label_text.set("초기 텍스트")
    label = tk.Label(search_star, textvariable=label_text)
    label.pack()

    for constellation_info in info:
        if constellation_name in constellation_info['TITLE']:
            label_text.set(constellation_info)
        else:
            label_text.set(text="해당하는 별자리 정보를 찾을 수 없습니다.")


def xml_parse():
 
    url = 'https://api.odcloud.kr/api/15067819/v1/uddi:bab0fa12-d7d7-4e47-975c-e35d424ae165?page=1&perPage=10&returnType=XML'

    service_key = "/ruEDWbFRa8SMf4ev1DPLwU307V7q7mQg9PPlx7euo7NQ+ktMmwxuICWtFUwJN8BKLv+HpKoHipHpOdeVE6qCw=="
    queryParams = {'serviceKey': service_key}

    response = requests.get(url, params=queryParams)
    print(response.text)
    print("\n")

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

window = tk.Tk()
window.title("지구별")
window.geometry("700x500")

string_var = tk.StringVar()

position="현 위치/설정한 위치"

string_var.set("지금 "+position+"의 하늘에는 ... ")

label = tk.Label(window, textvariable=string_var, font=("Helvetica", 15))
label.grid(row=0, column=0)

frame = tk.Frame(window)
frame.grid(row=0,column=1)

button = tk.Button(frame, text="별자리 검색하기", command=open_new_window)
button.pack()


OpenWebbutton = tk.Button(frame, text="하늘지도 열기", command=open_url)
OpenWebbutton.pack()

parsed_data = xml_parse()

# 파싱된 데이터 출력
for item in parsed_data:
    print(item)


'''
# 현재 위치 정보 가져오기
location = get_current_location()

if location is not None:
    latitude, longitude= location
    print("현재 위치 정보:")
    print("위도:", latitude)
    print("경도:", longitude)

else:
    print("위치 정보를 가져올 수 없습니다.")
'''


window.mainloop()
