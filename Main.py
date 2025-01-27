# starting with getting text from an image
# TODO: make bounding box more abstract make it find the cords it self so it can work on multiple devices
import easyocr
import os
import numpy as np
from PIL import ImageGrab
from PIL import Image
import time
import tkinter as tk
from groq import Groq
#get screen width and height
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()

print("Width:", width)
print("Height:", height)
#Taking screenshot
reader = easyocr.Reader(['en'])
bounding_box = (0,int(height/7),width,int(height/4))
time.sleep(2)
screenshot = ImageGrab.grab(bbox=bounding_box)
screenshot.save("temp.png")
result = reader.readtext(np.array(screenshot))
#result = reader.readtext("img_1.png")
s = ""
for(bbox,text,prob) in result:
    s = s+text
print(s, end=" ")
print("\n")




client = Groq(
    api_key= os.environ.get("GROQ_API_KEY")
)
message = s
completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": message
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)
response_text = completion.choices[0].message.content

'''
import tkinter as tk
import os
import numpy as np
from PIL import ImageGrab
from PIL import Image
import time
import tkinter as tk
import easyocr
img = Image.open("img_1.png")
img = img.convert("RGB")
img_array = np.array(img)
#E21B3C
red = [226, 27, 60]
blue = [19, 104, 206]
yellow =[199, 146, 0]
green = [38, 137, 12]
colors = [red,blue,yellow,green]
clickCoordsX = []
clickCoordsY = []
options = []
i = 0
reader = easyocr.Reader(['en'],gpu=True)
for color in colors:
    # Get X and Y coordinates of all blue pixels
    Y, X = np.where(np.all(img_array==color,axis=2))
    print(X[0],Y[0])
    print(X[len(X)-1],Y[len(Y)-1])
    clickCoordsX.append(int((X[(len(X) - 1) // 2])))
    clickCoordsY.append(int((Y[(len(Y) - 1) // 2])))
    tempimg = img.crop((int(X[0]),int(Y[0]),int(X[len(X)-1]),int(Y[len(Y)-1])))
    result = (reader.readtext(np.array(tempimg)))
    s = ""
    for (bbox, text, prob) in result:
        s = s + text
    options.append(s)
print(options)
print(clickCoordsX)
print(clickCoordsY)
'''






