import xml.etree.ElementTree as ET
from tkinter import *
import requests

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
    input_result.configure(text=in_text)
    findloc = print_dictionary(StarList, input_text.get())
    print(findloc)


#어디 있는지 찾아서 해당 딕션어리를 return
def print_dictionary(data, value):
    for dictionary in data:
        for key, inner_value in dictionary.items():
            if inner_value == value:
                temp_dict = dictionary  # 주어진 값이 있는 딕셔너리를 임시 변수에 저장
                return temp_dict
    print("없는 별지리")


#윈도우 만들기
window = Tk()
window.title("별자리 검색")
window.geometry('600x500')

label = Label(window, text="별자리를 찾아볼까요?",font=("돋음", 10))
label.grid(column=0, row=0)

input_text = Entry(window, width=30)
input_text.grid(column=0, row=2)

button = Button(window, text="확인", command=confirm)
button.grid(column=1, row=2)

input_result = Label(window, text="검색어:",font=("돋음", 10))
input_result.grid(column = 0,row = 3)

#받아온 값을 StarList에 넣어준다
StarList = XML_parse()

window.mainloop()