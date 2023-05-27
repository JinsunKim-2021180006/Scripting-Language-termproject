import xml.etree.ElementTree as ET
from tkinter import *
import requests


# 아래 함수를 매인에 추가(해더 잊지말기)

def search():
    # XML받아오기
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

        #검색 하기

    def confirm():
        in_text = "검색어 : " + input_text.get()
        findloc = print_dictionary(StarList, input_text.get())
        # print(findloc)
        printResult(findloc)


    #어디 있는지 찾아서 해당 딕션어리를 return
    def print_dictionary(data, value):
        for dictionary in data:
            for key, inner_value in dictionary.items():
                if inner_value == value:
                    temp_dict = dictionary  # 주어진 값이 있는 딕셔너리를 임시 변수에 저장
                    return temp_dict
        print("없는 별지리")


    def printResult(findInfo):
        global RenderText

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


    def firstSet():
        for i in range(len(StarList)):
            printResult(StarList[i])


    #윈도우 만들기
    searchwindow = Toplevel(window)
    searchwindow.title("별자리 검색")
    searchwindow.geometry('250x400')

    #상단 문구
    label = Label(searchwindow, text="별자리를 찾아볼까요?",font=("돋음", 10))
    label.grid(column=0, row=0)

    #입력창
    input_text = Entry(searchwindow, width=30)
    input_text.grid(column=0, row=2)

    #입력버튼
    button = Button(searchwindow, text="확인", command=confirm)
    button.grid(column=1, row=2)

    #아래에 출력하는 결과값(임시)
    printlist = Text(searchwindow,width=250,height=100)
    printlist.place(x=0,y=100)
    printlist.configure(state='disabled')

    #받아온 값을 StarList에 넣어준다
    StarList = XML_parse()

