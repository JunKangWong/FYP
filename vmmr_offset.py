# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 17:14:45 2021

@author: jkwon
"""
#import pandas as pd
# import operator
# import os, glob

from math import floor
from pathlib import Path
from collections import Counter
import shutil



class K_Fold_Validation(object):
    
    def __init__(self, myLst:list):
        self.lst = myLst
        
        
    def standard_compute_k(self, k:int): 
        percent = 1 / k   
        for i in range(1,k+1):    
            print(self.calculate_offset(i, percent))
    
    def standard_compute_percent(self, k:int, percent:int):
        if percent < 0 or percent > (1/k):
            print("Invalid Percent")
            return False
        
        for i in range(1,k+1):    
            print(self.calculate_offset(i, percent))
        
        return True
        
    def calculate_offset(self, fold:int, percent:float):
        list_of_offsets = []
        offset = 0
    
        for count in self.lst:
            # calculate current offset
            to_get = self.round_down_to_even(count*percent)
            res = int(offset + ((fold-1) * to_get))
            list_of_offsets.append((res, to_get))
            offset += count
            
        return list_of_offsets


    def round_down_to_even(self, num: int):
        res = floor(num)
        return res if res % 2 == 0 else res - 1




class File_Manipulation(object):
    
    def __init__(self, strPath:str, destPath:str, myK:int = 3, myPercent:int = 0.1):
        self.path = Path(strPath)
        self.dest = Path(destPath)
        self.files = sorted(list(self.path.glob("*")), key = lambda x: x.stem)
        self.k = myK

    
    def group_by_count(self):
        #df = pd.DataFrame()
        lst_of_names = []
        for filepath in self.files:
            lst = (filepath.stem).split("_")
            lst.pop()
            model = "_".join(lst)
            lst_of_names.append(model)

        my_dict = Counter(lst_of_names)
        #my_dict = sorted(my_dict.items(), key=operator.itemgetter(0))
        # return a list of occurences for each object in the file
        return my_dict.values()
    
    
    def locate_files(self, offset:int, count:int):
        """
        Given an offset and the number of item to copy. this function
        """
        return self.files[offset:offset+count]
    
    
    def compute_validation_set(self):
        lst = self.group_by_count()
        k_fold_validate = K_Fold_Validation(lst)
        
        offsets = k_fold_validate.calculate_offset(self.k, 0.13)
        lst_of_lsts = []

        for tup in offsets:
            lst = self.locate_files(tup[0], tup[1])
            lst_of_lsts.append(lst)
        
        return lst_of_lsts
        #k_fold_validate.standard_compute_percent(self.k, 0.1)
        
    
    def copy_to_destination(self):
        lst_of_lsts = self.compute_validation_set()

        for model in lst_of_lsts:
            for file in model:
                shutil.move(file, self.dest)
    



if __name__ == "__main__":
    lst = [124, 122, 118]
    data = K_Fold_Validation(lst)

    from_path_str = r"C:\Users\jkwon\Desktop\Cross Validation\Train3"
    to_path_str = r"C:\Users\jkwon\Desktop\Cross Validation\Validation3"
    #k = File_Manipulation(from_path_str, to_path_str)
    k = File_Manipulation(from_path_str, to_path_str)
    k.copy_to_destination()

    #k = 3
    #print(data.calculate_offset(1, 0.2))
    #data.standard_compute_percent(k, 0.1)
    #data.standard_compute_k(k)
    
    #print(len(k.group_by_count()))
    
    #for item in k.group_by_count():
        #print(item)
        #print(k.group_by_count())
    
   # print(k.locate_files(5, 13))
    
    #k.compute_validation_set()
    #k.copy_to_destination()