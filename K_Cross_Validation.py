# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 17:14:45 2021

@author: jkwon
"""
from math import floor
from pathlib import Path
from collections import Counter
import shutil



class K_Fold_Validation(object):
    """
    Given a list of count for the specified data of each car model.
    This class generate an offset and a count for K-fold cross validation
    depending on the list.
    """
    def __init__(self, myLst:list):
        self.lst = myLst
        
        
    def standard_compute_k(self, k:int):
        """
        This function computes and print the offset and count of the validation set 
        based on the number of folds specified.
        Parameters
        ----------
        k : int
            DESCRIPTION.
            the number of folds k of the k-fold validation.

        Returns
        -------
        None.

        """
        percent = 1 / k   
        for i in range(1,k+1):    
            print(self.calculate_offset(i, percent))
    
    def standard_compute_percent(self, k:int, percent:int):
        """
        This function computes and print k-fold based on percentage specified.
        """
        if percent < 0 or percent > (1/k):
            print("Invalid Percent")
            return False
        
        for i in range(1,k+1):    
            print(self.calculate_offset(i, percent))
        
        return True
        
    def calculate_offset(self, fold:int, percent:float):
        """
        This function is the main function for offset calculation and count calculation
        of the k-fold validation.
        
        Return: list of tuple (offset, count), where offset is the offset to start the 
        of the validation set and count is the number of element that belongs to that
        validation set.
        """
        list_of_offsets = []
        offset = 0
    
        for count in self.lst:
            # calculates count
            to_get = self.round_down_to_even(count*percent)
            
            # calculate current offset
            res = int(offset + ((fold-1) * to_get))
            
            # put both the offset and count into a list.
            list_of_offsets.append((res, to_get))
            
            # increment offset by count.
            offset += count
        
        # return the list of tuples
        return list_of_offsets


    def round_down_to_even(self, num: float):
        """
        This function takes in a number and round down the number to the next closest
        even number.
        
        Return int, number round down to the closest even number.
        """
        res = floor(num)
        
        # if number after round down to integer is not even,  minus 1 to become even.
        return res if res % 2 == 0 else res - 1




class File_Manipulation(object):
    """
    This class manipulates files of FIT3162 VMMR project. Files musts be saved in 
    the following format for this class to work.
    
    brand_D_XXX, where,
    brand   : is the car brand or model of the car
    D       : The direction of the car, R indicate Right, L indicate left, unspecified indicate front.
    XXX     : number label of the data.
    
    Both the label files and image file are expected to be saved in the same format.
    """
    
    def __init__(self, strPath:str, destPath:str, myK:int = 3, myPercent:int = 0.13):
        self.path = Path(strPath)
        self.dest = Path(destPath)
        self.files = sorted(list(self.path.glob("*")), key = lambda x: x.stem)
        self.k = myK
        self.percent = myPercent

    
    def group_by_count(self):
        """
        This function assumes that the folder contain files in the format 
        brand_D_001.txt Such that brand_D can be uniquely identified. Based
        on the files in self.path this function computes a list of count (integer)
        specifying the number of data for each car model.
        
        Returns
        -------
        my_dict.values() : TYPE list of integer
            DESCRIPTION. a list of count (integer)
            specifying the number of data for each car model.
        """
        lst_of_names = []
        for filepath in self.files:
            lst = (filepath.stem).split("_")
            lst.pop()
            model = "_".join(lst)
            lst_of_names.append(model)

        my_dict = Counter(lst_of_names)
        
        return my_dict.values()
    
    
    def locate_files(self, offset:int, count:int):
        """
        Given an offset and the number of item to copy. this function make a list
        containing a list of file Paths containing path in that interval.
        
        Returns
        -------
        self.files[offset:offset+count],  a list of file Paths containing path in that interval.
        """
        return self.files[offset:offset+count]
    
    
    def compute_validation_set(self):
        """
        This function filters out the file Path of files to be copied to the 
        validation set based on K_Fold_Validation calculations.
    
        Returns
        -------
        lst_of_lsts : TYPE list in list of type Path
            DESCRIPTION. contains generated Path element to be moved to 
            validation set.
        """
        # generate list of count list for k_fold_calculation.
        # generate a list of offsets and number of elements to be copied.
        lst = self.group_by_count()
        k_fold_validate = K_Fold_Validation(lst) 
        
        offsets = k_fold_validate.calculate_offset(self.k, self.percent)
        lst_of_lsts = []

        for tup in offsets:
            lst = self.locate_files(tup[0], tup[1])
            lst_of_lsts.append(lst)
        
        return lst_of_lsts        
    
    def move_to_destination(self):
        """
        This function copies the files specified in the lst_of_lsts and move them 
        to the destination.

        Returns
        -------
        None.

        """
        lst_of_lsts = self.compute_validation_set()

        for model in lst_of_lsts:
            for file in model:
                shutil.move(file, self.dest)
    



if __name__ == "__main__":
    lst = [124, 122, 118]
    data = K_Fold_Validation(lst)

    from_path_str = r"from path"
    to_path_str = r"to path"
    #k = File_Manipulation(from_path_str, to_path_str)
    k = File_Manipulation(from_path_str, to_path_str)
    k.move_to_destination()

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