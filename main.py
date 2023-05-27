import requests
import xml.etree.ElementTree as ET
from tkinter import *



def UpLoadData():
    
    url = 'https://api.odcloud.kr/api/15067819/v1/uddi:bab0fa12-d7d7-4e47-975c-e35d424ae165?page=1&perPage=10&returnType=XML'

    service_key = "/ruEDWbFRa8SMf4ev1DPLwU307V7q7mQg9PPlx7euo7NQ+ktMmwxuICWtFUwJN8BKLv+HpKoHipHpOdeVE6qCw=="
    queryParams = {'serviceKey': service_key}

    response = requests.get(url, params=queryParams)
    print(response.text)

    queryURL = url+queryParams
    response = requests.get(queryURL)
    print(response.text)


def Main():
    window = Tk()
    window.title("지구별")
    window.geometry("800x600")
    window.configure(bg="indigo")

    UpLoadData()

    window.mainloop()


Main()