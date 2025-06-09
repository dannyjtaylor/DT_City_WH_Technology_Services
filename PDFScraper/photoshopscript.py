import pandas as pd
import os
import cv2




for file in os.listdir("\\\\howard\\01 - Technology Services\\13 - Media Files\\03 - ID Badges\\03 - Jostle Pictures\\03 - ALL Photos"):
    if file.endswith(".jpg"):
        # read the image
        img = cv2.imread("\\\\howard\\01 - Technology Services\\13 - Media Files\\03 - ID Badges\\03 - Jostle Pictures\\03 - ALL Photos\\" + file)
        # get the dimensions of the image
        height, width, channels = img.shape
        # print the dimensions
        print(f"{file}: {height}x{width}x{channels}")
        # check if the image is 300x300 pixels