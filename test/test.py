import tkinter as tk
import requests

url = 'http://server2.sky-map.org/search'

temp = input()
queryParams = {'request': temp}

response = requests.get(url, params=queryParams)
print(response.text)
