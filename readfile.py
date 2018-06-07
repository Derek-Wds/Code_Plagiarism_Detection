# -*- coding: utf-8 -*- 

import os
from utils import *

def read_file(f):
    f = open(f, encoding="utf8")
    codes = f.readlines()
    num = 0
    while True:
        try:
            if "//" in codes[num] or "@" in codes[num]:
                del codes[num]
            else:
                num += 1
        except:
            break
    code = ''.join(codes)
    test = polish(code)
    w = winnow(test)
    f.close()
    return w


def get_file(file_dir): 
    file_dic = {}
    num = 0
    for root, dirs, files in os.walk(file_dir):
        # print("root", root) #current root
        # print("dirs", dirs) #current directories
        # print("files", files) #current files (not directory)
        if files is None:
            pass
        elif ".xml" in str(files):
            pass
        elif ".java" in str(files) or ".groovy" in str(files):
            if "test" in str(files) or "Test" in str(files) or "test" in str(root) or "Test" in str(root):
                pass
            else:
                for i in files:
                    f = open(root + "\\" + i, encoding="utf8")
                    codes = f.readlines()
                    while True:
                        try:
                            if "//" in codes[num]:
                                del codes[num]
                            else:
                                num += 1
                        except:
                            break
                    code = ''.join(codes)
                    a = ''.join(comment_del(code.lower().split()))
                    if "interface" in a:
                        pass
                    elif "abstractclass" in a and not "return" in a:
                        pass
                    elif "class" not in a:
                        pass
                    else:
                        try:
                            file_dic[num]["files"].append(i)
                        except:
                            file_dic[num] = {"root":root, "dirs":dirs, "files":[i]}
                num += 1
        else:
            pass
    return file_dic
