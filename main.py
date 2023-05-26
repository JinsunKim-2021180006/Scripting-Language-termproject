import requests
import xml.etree.ElementTree as ET
import tkinter

url = 'https://api.odcloud.kr/api/15067819/v1/uddi:bab0fa12-d7d7-4e47-975c-e35d424ae165?page=1&perPage=10&returnType=XML'

service_key = "/ruEDWbFRa8SMf4ev1DPLwU307V7q7mQg9PPlx7euo7NQ+ktMmwxuICWtFUwJN8BKLv+HpKoHipHpOdeVE6qCw=="
queryParams = {'serviceKey': service_key}

response = requests.get(url, params=queryParams)
print(response.text)

queryURL = url+queryParams
response = requests.get(queryURL)
print(response.text)


window = tkinter.Tk()
window.title("지구별")

frame = tkinter.Frame(window)
frame.pack()