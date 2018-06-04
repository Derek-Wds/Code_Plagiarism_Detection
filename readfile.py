# -*- coding: utf-8 -*- 

import os

def get_file(file_dir): 
    file_dic = {}
    num = 0
    for root, dirs, files in os.walk(file_dir):
        # print("root", root) #current root
        # print("dirs", dirs) #current directories
        # print("files", files) #current files (not directory)
        if files is None:
            pass
        elif ".java" in str(files):
            file_dic[num] = {"root": root, "dirs": dirs, "files": files}
            num += 1
        else:
            pass
    return file_dic
