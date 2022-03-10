# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 19:46:35 2021

@author: jkwon
"""

from pathlib import Path


class File_Manipulation(object):
    
    def __init__(self, strPath:str):
        self.path = Path(strPath)
        self.files = list(self.path.glob("*(*)*"))


    def get_wrong_format(self):
        for path in self.files:
            lst = path.stem.split(" ")
            ext = path.suffix
            num = lst[1][1:-1]
            newname = lst[0] +  "_" + num + ext
            directory = path.parent
            
            path.rename(Path(directory, newname))
            
   
if __name__ == "__main__":
    str_path = r"C:\Users\jkwon\Desktop\test_dataset"
    k = File_Manipulation(str_path)
    k.get_wrong_format()