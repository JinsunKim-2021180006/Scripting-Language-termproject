#pip install clipboard
import clipboard
import requests
from tkinter import *
from tkinter.ttk import *
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk



def parse_xml(xml_data):
    result_dict = {}
    root = ET.fromstring(xml_data)
    items = root.find('body/items')
    if items is not None:
        for item in items.findall('item'):
            astro_title = item.find('astroTitle')
            astro_event = item.find('astroEvent')
            if astro_title is not None:
                result_dict[astro_title.text] = astro_event.text
            else: 
                result_dict['0'] = '0'
    return result_dict

def printData(DATA_DIC, printlist):
    printlist.configure(state='normal')
    printlist.delete("0.0","end")
    if len(DATA_DIC) == 0:
        printlist.insert("end","해당 일자에 일어난 사건이 없습니다.")
    else:
        for title, event in DATA_DIC.items():
            if title is not None:
                printlist.insert("end","사건 이름: ")
                printlist.insert("end",title or "")
                printlist.insert("end","\n")
                printlist.insert("end","사건 내용: ")
                printlist.insert("end",event)
                printlist.insert("end","\n")
        printlist.configure(state='disabled')

def listcopy(printlist):
    text_value = printlist.get("1.0", "end-1c")
    clipboard.copy(text_value)

def upload_xml(Year, month, printlist):
    url = 'http://apis.data.go.kr/B090041/openapi/service/AstroEventInfoService/getAstroEventInfo'
    service_key = "Nt9JLubbJypY+2kCOW3BhPuQjwuYm0o7eHRKSvBxk7aUk/CI9KgBzv06qHctRy26s56jTjqI0kdOKj1gy3oI8Q=="
    queryParams = {'serviceKey' : service_key, 'solYear' : Year.get(), 'solMonth' : month.get()}
    response = requests.get(url, params=queryParams)
    xmldata = response.content

    Data_Dic = parse_xml(xmldata)
    printData(Data_Dic, printlist)


def create_window_background(window):
    image = Image.open("resource/sbg.jpg")
    resized_image = image.resize((820, 400))
    photo = ImageTk.PhotoImage(resized_image)

    BG_label = Label(window, image=photo)
    BG_label.place(x=0, y=0, relwidth=1, relheight=1)

    # 반환하여 전역 변수로 유지
    return photo


def pastsearch():
    subsearchwindow = Toplevel()
    subsearchwindow.title("과거 천체 현상 검색")
    subsearchwindow.geometry('300x400')
    subsearchwindow.config(bg="#231B61")

    photo = create_window_background(subsearchwindow)

    label = Label(subsearchwindow, text="★의 ★일",font=("Helvetica", 15), background="#231B61",foreground="white")
    label.place(x=50,y=10)

    Year = Combobox(subsearchwindow)
    Year['values'] = ( "2016","2017","2018","2019","2020","2021","2022")
    Year.set("검색할 연도")
    Year.config(state="readonly")
    Year.place(x=50, y=50)
    
    month = Combobox(subsearchwindow)
    month['values'] = ( "01","02","03","04","05","06","07","08","09","10","11","12")
    month.set("검색할 달")
    month.config(state="readonly")
    month.place(x=50,y=80)
    
    go = Button(subsearchwindow, text="검색", command=lambda: upload_xml(Year, month, printlist))
    go.place(x=50,y=110)
    copyButton = Button(subsearchwindow, text="복사하기", command=lambda: listcopy(printlist))
    copyButton.place(x=150,y=110)

    printlist = Text(subsearchwindow,width=30,height=20, wrap="word")
    printlist.place(x=50,y=150)
    printlist.configure(state='disabled')
    
    subsearchwindow.mainloop()
