import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import *

from opensite import *
import PastSearch
import search
#pip install geocoder
import geocoder

def gosearch():
    search.Search(window)


def subsearch():
    PastSearch.pastsearch()
    
 

# 현재 위치의 위도와 경도 가져오기
g = geocoder.ip('me')
latitude, longitude = g.latlng

# 현재 위치의 위도와 경도 출력
print(latitude, longitude)


window = tk.Tk()
window.title("지구별")
window.geometry("700x500")

string_var = tk.StringVar()

position="현 위치/설정한 위치"

string_var.set("지금 "+"위도:" + str(latitude) + "경도:" + str(longitude) +"의 하늘에는 ... ")

label = tk.Label(window, textvariable=string_var, font=("Helvetica", 15))
label.place(x=150,y=0)

frame = tk.Frame(window)
frame.place(x=150, y=30)

button = tk.Button(frame, text="별자리 검색하기", command=gosearch)
button.pack()


OpenWebbutton = tk.Button(frame, text="하늘지도 열기", command=open_url)
OpenWebbutton.pack()

button = tk.Button(frame, text="과거 천체 현상 검색", command=subsearch)
button.pack()





window.mainloop()
