import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import Style

from opensite import *
import PastSearch
import search
import cv2
import teller

#pip install geocoder
import geocoder


def gosearch():
    search.Search(window)


def subsearch():
    PastSearch.pastsearch()


def tel():
    teller.window()


video_path ="resource/bg.gif"
video = None
vlabel =None
framesub =None
def InitVideo():
    global video ,video_path,vlabel ,frame
    # 비디오 파일 열기
    video = cv2.VideoCapture(video_path)

    # 비디오 크기 가져오기
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 비디오 프레임 표시할 레이블 생성
    vlabel = Label(framesub, width=820, height=400)
    vlabel.place(x=0, y=30)

    # 비디오 플레이어 시작
    show_frame()


def show_frame():
    global video, video_path, vlabel
    # 비디오 프레임 읽기
    ret, frame = video.read()

    if ret:
        # 프레임을 PIL 이미지로 변환
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        photo = ImageTk.PhotoImage(image)

        # 레이블에 이미지 표시
        vlabel.config(image=photo)
        vlabel.image = photo


    else:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 비디오 위치를 처음으로 되돌림
    # 다음 프레임을 표시하기 위해 함수 재호출
    window.after(30, show_frame)







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

InitVideo()
framesub = window

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


#텔레그램 버튼 추가
image = Image.open("resource/tel.png")
resized_image = image.resize((100, 100))
photo_image = ImageTk.PhotoImage(resized_image)

historyButton = tk.Button(window, image=photo_image, command=tel)
historyButton.image = photo_image
historyButton.config(width=80, height=80)
historyButton.place(x=270,y=30)


window.mainloop()
