from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
import gps
import weather



latitude, longitude = gps.latitude,gps.longitude
api_key = "AIzaSyDrpg0DcFwffvsWKL8q1mQoJ5-2j4c8K9w"
weather_inform=weather.lookUpWeather()

def show_map(latitude, longitude, api_key):
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom=13&size=600x300&key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        image_data = response.content

        root = Tk()
        root.title("Google Map")

        canvas = Canvas(root, width=600, height=300)
        canvas.pack()

        image = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))
        canvas.create_image(0, 0, anchor="nw", image=image)

        root.mainloop()
    else:
        print("구글 맵을 불러오는데 실패했습니다.")



def window():
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom=13&size=600x300&key={api_key}"
    response = requests.get(url)

    image_data = response.content

    weatherwindow = Toplevel()
    weatherwindow.title("위치/날씨정보")
    weatherwindow.geometry('500x300')

    label = Label(weatherwindow, text=weather_inform, font=("Helvetica", 15), foreground="white",background="indigo")
    label.grid(column=0, row=0)

    canvas = Canvas(weatherwindow, width=500, height=300)
    canvas.grid(column=0, row=1)

    image = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))
    canvas.create_image(0, 0, anchor="nw", image=image)

    weatherwindow.mainloop()



if __name__ == "__main__":
    show_map(latitude, longitude, api_key)
