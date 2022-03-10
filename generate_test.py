# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 12:51:39 2021

@author: jkwon
"""

# https://github.com/theAIGuysCode/YOLOv4-Cloud-Tutorial/blob/master/yolov4/generate_test.py


import os

image_files = []
os.chdir(os.path.join("data", "test"))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        image_files.append("data/test/" + filename)
os.chdir("..")
with open("test.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()
os.chdir("..")