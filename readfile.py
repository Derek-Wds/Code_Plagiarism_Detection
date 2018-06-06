# -*- coding: utf-8 -*- 

import os
from utils import *

def read_file(f):
    f = open(f, encoding="utf8")
    codes = f.readlines()
    num = 0
    while True:
        try:
            if "//" in codes[num]:
                del codes[num]
            else:
                num += 1
        except:
            break
    code = ''.join(codes)
    test = polish(code)
    w = winnow(test)
    f.close()
    return ''.join(test)


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
            if "test" in str(files) or "Test" in str(files) or "test" in str(root) or "Test" in str(root):
                pass
            else:
                file_dic[num] = {"root": root, "dirs": dirs, "files": files}
                num += 1
        else:
            pass
    return file_dic
