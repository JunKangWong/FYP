# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 20:59:14 2021

File manipulation

@author: Wong Jun Kang
"""
# pathlib: https://docs.python.org/3/library/pathlib.html
from pathlib import Path


class file_metadata(object):
    """
    This class specifies the class metadata required for file manipulations.
    """
    # .jpg by default
    def __init__(self, path:Path, ext: str='.jpg', savepath:Path = None):
        self.my_path = path
        self.my_ext = ext
        self.my_savepath = savepath
        


def change_file_name(metadata: file_metadata, filename: str):
    """
    This function takes in file_metadata object and filename. Then proceeds to 
    rename files based on filename specified such that file 1 --> filename001.ext,
    file2 --> filename002.ext ..... fileN --> filename00N.ext.

    Parameters
    ----------
    metadata : file_metadata
        DESCRIPTION: file information, such as file path, extension. save path etc.
    filename : str
        DESCRIPTION: filename_to_change into
    Returns
    -------
    None.

    """
    # Get file metadata and put the Path object of files with specified extensions into a list.
    ext, path = metadata.my_ext, metadata.my_path
    imgs = list(path.glob('*'+ ext))
    
    # loop through 
    for i, img in enumerate(imgs):
        # useful in situation where file type is not specified. (can be commented otherwise).
        ext = img.suffix    
        directory = img.parent
        new_name = "{}{:03}{}".format(filename, i+1, ext)
        img.rename(Path(directory, new_name))


if __name__ == "__main__":
    # Specify the path for the files you want to manipulate.
    path_str = r"C:\Users\jkwon\Desktop\Processed_side_images\perodua_sides\viva_side\R"
    path = Path(path_str)
    
    # Specify file information
    # specify "" to change all names regardless of file type
    file_ext = ['.txt', '.jpg', '.png', '.jpeg', ""]
    metadata = file_metadata(path)
    
    # Change filename
    filename = "peroduaViva_R_"  # filename to change into
    change_file_name(metadata, filename)

    
    
    
    