import tkinter as tk
import webview

def open_url():
    url = 'http://www.skymaponline.net/'  # 여기에 열고자 하는 URL을 입력하세요
    webview.create_window('Web Content', url=url)
    webview.start()

# tkinter 창 생성
window = tk.Tk()

# 버튼 생성
button = tk.Button(window, text='Open Website', command=open_url)
button.pack()

# tkinter 이벤트 루프 시작
window.mainloop()
