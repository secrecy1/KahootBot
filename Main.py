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
bounding_box = (0,height/7,width,height/4)
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
'''
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
'''



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

img = ImageGrab.grab(bbox=(0,int(height/2),width,height))
img.save("FREE.png")
print("AI response")
print(response_text)
# Convert the image to grayscale
gray_img = img.convert("L")  # "L" mode converts to grayscale

# Convert the grayscale image to a NumPy array for fast processing
gray_array = np.array(gray_img)

# Define the target grayscale value (0-255)
target_gray_value = 90  # Replace with your desired grayscale value

# Find the pixel coordinates of the closest match
difference = np.abs(gray_array - target_gray_value)
min_diff = np.min(difference)
coordinates = np.argwhere(difference == min_diff)
#bounding_box = (0,height/7,width,height/4)

#screenshot2 = ImageGrab.grab()
#screenshot2.save("temp.png")
# Print the results
xMax = 0
yMax = 0
if len(coordinates) > 0:
    print(f"Pixel(s) with closest match to {target_gray_value}:")
    for coord in coordinates:
        print(f"Row: {coord[0]}, Column: {coord[1]}")
        xMax = max(coord[0],xMax)
        yMax = max(coord[0], yMax)

else:
    print("No matching pixel found.")
yMax = yMax + int(height / 2)
bounding_box = [0,0,xMax,yMax]
screenshot2 = ImageGrab.grab(bbox = bounding_box)
screenshot2.save("tester.png")





