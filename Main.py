# starting with getting text from an image
# TODO: make bounding box more abstract make it find the cords it self so it can work on multiple devices
from contextlib import nullcontext

import easyocr
import numpy as np
from PIL import ImageGrab
from PIL import Image
import time
import tkinter as tk

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()

print("Width:", width)
print("Height:", height)
reader = easyocr.Reader(['en'])
bounding_box = (0,height/8.7,width,height/4)
time.sleep(10)
screenshot = ImageGrab.grab(bbox=bounding_box)
screenshot.save("temp.png")
result = reader.readtext(np.array(screenshot))
#result = reader.readtext("img_1.png")
for(bbox,text,prob) in result:
    print(text,end=" ")
print("\n")

# Load image, ensure not palettised, and make into Numpy array
pim = Image.open('img_1.png').convert('RGB')
im  = np.array(pim)

# Define the blue colour we want to find - PIL uses RGB ordering
color = [255,255,255]

# Get X and Y coordinates of all blue pixels
#np.set_printoptions(threshold=np.inf)
step = 1
Y, X = np.where(np.all(im[::step, ::step] == color, axis=2))

# Scale back coordinates to match original image
Y = Y * step
X = X * step


print("colors")
print("X: ",end="")
print(X)
print("-------------------------")
print("Y: ",end="")
print(Y)




