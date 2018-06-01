# -*- coding: utf-8 -*- 

import os

def file_name(file_dir): 
    for root, dirs, files in os.walk(file_dir):
        print("root", root) #current root
        print("dirs", dirs) #current directories
        print("files", files) #current files (not directory)
