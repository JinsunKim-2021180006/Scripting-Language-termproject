import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import Style

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



window = tk.Tk()
window.title("지구별")
window.geometry("820x400")

image = Image.open("resource/bg.jpg")
resized_image = image.resize((820, 400))
window.config(bg="white")
photo = ImageTk.PhotoImage(resized_image)
BG_label = Label(window, image=photo)
BG_label.place(x=0, y=0, relwidth=1, relheight=1)  # 전체 창 크기에 맞춰 배경 이미지 표시


string_var = tk.StringVar()

position="현 위치/설정한 위치"

string_var.set("지금 "+"위도:" + str(latitude) + "경도:" + str(longitude) +"의 하늘에는 ... ")

label = tk.Label(window, textvariable=string_var, font=("Helvetica", 15),bg="indigo",fg="white")
label.place(x=0,y=0)



#버튼 설정
image = Image.open("resource/search.png")
resized_image = image.resize((100, 100))
photo_image = ImageTk.PhotoImage(resized_image)

button = tk.Button(window, image=photo_image, command=gosearch)
button.image = photo_image
button.config(width=80, height=80)
button.place(x=0,y=30)



image = Image.open("resource/map.png")
resized_image = image.resize((100, 100))
photo_image = ImageTk.PhotoImage(resized_image)

OpenWebbutton = tk.Button(window, image=photo_image, command=open_url)
OpenWebbutton.image = photo_image
OpenWebbutton.config(width=80, height=80)
OpenWebbutton.place(x=90,y=30)

image = Image.open("resource/his.png")
resized_image = image.resize((100, 100))
photo_image = ImageTk.PhotoImage(resized_image)

historyButton = tk.Button(window, image=photo_image, command=subsearch)
historyButton.image = photo_image
historyButton.config(width=80, height=80)
historyButton.place(x=180,y=30)



window.mainloop()
