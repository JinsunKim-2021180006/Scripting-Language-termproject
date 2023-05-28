import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

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
window.geometry("410x200")

image = Image.open("resource/bg.jpg")
resized_image = image.resize((700, 500))
window.config(bg="white")
photo = ImageTk.PhotoImage(resized_image)
BG_label = Label(window, image=photo)
BG_label.place(x=0, y=0, relwidth=1, relheight=1)  # 전체 창 크기에 맞춰 배경 이미지 표시


string_var = tk.StringVar()

position="현 위치/설정한 위치"

string_var.set("지금 "+"위도:" + str(latitude) + "경도:" + str(longitude) +"의 하늘에는 ... ")

label = tk.Label(window, textvariable=string_var, font=("Helvetica", 15))
label.place(x=0,y=0)

button = tk.Button(window, text="별자리 검색하기", command=gosearch, bg="black", fg="white")
button.place(x=0,y=30)


OpenWebbutton = tk.Button(window, text="하늘지도 열기", command=open_url, bg="black", fg="white")
OpenWebbutton.place(x=0,y=60)

button = tk.Button(window, text="과거 천체 현상 검색", command=subsearch, bg="black", fg="white")
button.place(x=0,y=90)





window.mainloop()
