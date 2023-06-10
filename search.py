#pip install clipboard
import clipboard
import requests
import xml.etree.ElementTree as ET
from tkinter import *
from PIL import Image, ImageTk

#pip install pywebview
import webview
import fileio

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

def print_dictionary(data, value):
    for dictionary in data:
        for key, inner_value in dictionary.items():
            if inner_value == value:
                temp_dict = dictionary  # 주어진 값이 있는 딕셔너리를 임시 변수에 저장
                return temp_dict
    print("없는 별지리")


def listcopy(printlist):
    text_value = printlist.get("1.0", "end-1c")
    clipboard.copy(text_value)


def printResult(findInfo, printlist):
    datalist = []

    name = findInfo['TITLE']                #이름
    season = findInfo['D_SUMMARY']          #별이 뜨는 계절
    position = findInfo['POSITION']         #위치
    engName = findInfo['SCIENTIFIC_NM']     #영어이름
    starcount = findInfo['STAR_COUNT']      #별자리를 이루는 별 개수

    datalist.append(name)
    datalist.append(season)
    datalist.append(position)
    datalist.append(engName)
    datalist.append(starcount)

    printlist.configure(state='normal')
    printlist.delete("0.0","end")

    printlist.insert("end","별자리 이름: ")
    printlist.insert("end",datalist[0]+"\n")
    printlist.insert("end","보이는 계절: ")
    printlist.insert("end",datalist[1]+"\n")
    printlist.insert("end","위치: ")
    printlist.insert("end",datalist[2]+"\n")
    printlist.insert("end","영어 이름: ")
    printlist.insert("end",datalist[3]+"\n")
    printlist.insert("end","별 개수: ")
    printlist.insert("end",datalist[4]+"\n\n")
    printlist.configure(state='disabled')

def confirm(where, input_text, printlist, StarList):
    findloc = print_dictionary(StarList, input_text.get())
    if where == 0:
        printResult(findloc, printlist)
    else:
        openstarmap(findloc)


def openstarmap(datalist):
    
    engName = datalist['SCIENTIFIC_NM']     #영어이름

    url = "http://www.sky-map.org/?show_constellation_boundaries=0&zoom=2" +"&object=" + engName
    webview.create_window('Web Content', url=url,min_size=(800, 600))
    webview.start()

def create_window_background(window):
    image = Image.open("resource/sbg.jpg")
    resized_image = image.resize((820, 400))
    photo = ImageTk.PhotoImage(resized_image)

    BG_label = Label(window, image=photo)
    BG_label.place(x=0, y=0, relwidth=1, relheight=1)

    # 반환하여 전역 변수로 유지
    return photo


def Search(window):
    searchwindow = Toplevel(window)
    searchwindow.title("별자리 검색")
    searchwindow.geometry('350x300')
    searchwindow.config(bg="#231B61")

    photo = create_window_background(searchwindow)
    
    label = Label(searchwindow, text="★ 검색하기",font=("Helvetica", 15), background="#231B61",foreground="white")
    label.place(x=50,y=10)
    
    input_text = Entry(searchwindow, width=20)
    input_text.place(x=50, y=50)

    button = Button(searchwindow, text="검색", command=lambda: confirm(0,input_text, printlist, StarList),highlightthickness=0)
    button.place(x=250, y=50)
    copyButton = Button(searchwindow, text="복사하기", command=lambda: listcopy(printlist))
    copyButton.place(x=50,y=80)
    gomapButton = Button(searchwindow, text="내보내기", command=lambda: fileio.save_to_file(printlist))
    gomapButton.place(x=150,y=80)
    gomapButton = Button(searchwindow, text="별 보러가기", command=lambda: confirm(1,input_text,printlist,StarList))
    gomapButton.place(x=250,y=80)
    

    printlist = Text(searchwindow,width=35,height=12)
    printlist.place(x=50,y=120)
    printlist.configure(state='disabled')

    StarList = XML_parse()
    
    searchwindow.mainloop()
    
    