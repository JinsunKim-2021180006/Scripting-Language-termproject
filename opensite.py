#pip install pywebview
import webview

def open_url():
    url = 'http://www.skymaponline.net/' 
    webview.create_window('Web Content', url=url)
    webview.start()
