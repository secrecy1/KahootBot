# starting with getting text from an image
import time
start_time = time.perf_counter()
import easyocr
import os
import numpy as np
from PIL import ImageGrab
import tkinter as tk
from groq import Groq
from PIL import ImageFilter
import pyautogui
import turtle
import keyboard


print(time.perf_counter() - start_time)

start_time = time.perf_counter()
#get screen width and height
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()


#print("Width:", width)
#print("Height:", height)
#Taking screenshot
def solve():
    reader = easyocr.Reader(['en'],gpu = True)
    bounding_box = (0,int(height/7),width,int(height/4))
    b2 = (0,int(height/2),width,int(height/1.35))
    rImage = ImageGrab.grab()
    print(time.perf_counter() - start_time)
    screenshot = rImage.crop(bounding_box)
    s2 = rImage.crop(b2)
    s2.save("wow.png")
    #screenshot.save("temp.png")
    result = reader.readtext(np.array(screenshot)) or reader.readtext(np.array(s2))
    #result = reader.readtext("img_1.png")
    sq = ""

    for(bbox,text,prob) in result:
        sq = sq+text
    print(time.perf_counter() - start_time)
    #print(sq, end=" ")
    #print("\n")






    img = rImage.crop((0,int(height * .6),width,int(height* .95)))
    #img.save("whatthesigmawhyisntthisworking.png")
    img = img.convert("RGB")
    img = img.filter(ImageFilter.GaussianBlur(1.5))
    img_array = np.array(img)
    print(time.perf_counter() - start_time)

    # Define color ranges (lower and upper bounds)
    red_range = ([226, 27, 60], [240,45,70])
    blue_range = ([19, 104, 206], [20,114,216])
    yellow_range = ([199, 146, 0], [216,158,2])
    green_range = ([38, 137, 12], [39,137,13])
    color_ranges = [red_range, blue_range, yellow_range, green_range]

    clickCoordsX = []
    clickCoordsY = []
    options = []
    print(time.perf_counter() - start_time)
    for lower, upper in color_ranges:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        # Get X and Y coordinates of all matching pixels within the range
        Y, X = np.where(np.all((img_array >= lower) & (img_array <= upper), axis=2))

        if len(X) == 0 or len(Y) == 0:
            print("Color not found ")
            continue  # Skip if no pixels found
        #print(len(X))
        #print(Y)
        #print(X[0], Y[0])
        #print(X[-1], Y[-1])

        # Store the middle pixel coordinates
        clickCoordsX.append(int(X[(len(X) - 1) // 2]))
        #re scale y cords
        clickCoordsY.append(int((int(Y[(len(Y) - 1 ) // 2])) + height* 0.6))

        # Crop the region containing the color
        tempimg = img.crop((int(X[0]), int(Y[0]), int(X[-1]), int(Y[-1])))


        # Perform OCR on the cropped region
        result = reader.readtext(np.array(tempimg))
        s = ""
        for (bbox, text, prob) in result:
            s = s + text
        options.append(s)
    #print(time.perf_counter() - start_time)
    #print(options)
    #print(clickCoordsX)
    #print(clickCoordsY)
    client = Groq(
        api_key= os.environ.get("GROQ_API_KEY")
    )
    message = sq
    message = message + " Your options are "
    i = 0
    for opt in options:
        message = message + chr(97+i) + ". " + opt + " "
        i = i + 1
    #print(message)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": message +" only return exactly one character corresponding to the correct option"
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    response_text = completion.choices[0].message.content
    #print(response_text)
    pyautogui.moveTo(clickCoordsX[ord(response_text) - 97], clickCoordsY[ord(response_text) - 97])
    #print()
    #print(clickCoordsX[ord(response_text) -97])
    #print(clickCoordsY[ord(response_text) -97])
    pyautogui.click()
    end_time = time.perf_counter()
    print(end_time - start_time)
while True:
    if keyboard.is_pressed('b'):
        try:
            solve()
        except:
            pass
    elif keyboard.is_pressed('esc'):
        break





