# starting with getting text from an image
# TODO: make bounding box more abstract make it find the cords it self so it can work on multiple devices
import easyocr
import numpy as np
from PIL import ImageGrab
from PIL import Image
import time
reader = easyocr.Reader(['en'])
bounding_box = (300,300,800,800)
#time.sleep(10)
#screenshot = ImageGrab.grab(bbox=bounding_box)
#screenshot.save("temp.png")
#result = reader.readtext(np.array(screenshot))
result = reader.readtext("img_1.png")
for(bbox,text,prob) in result:
    print(text,end=" ")
print("\n")

# Load image, ensure not palettised, and make into Numpy array
pim = Image.open('img_1.png').convert('RGB')
im  = np.array(pim)

# Define the blue colour we want to find - PIL uses RGB ordering
color = [255,255,255]

# Get X and Y coordinates of all blue pixels
np.set_printoptions(threshold=np.inf)
Y, X = np.where(np.all(im==color,axis=2))
print("colors")
print(X)
print(Y)




