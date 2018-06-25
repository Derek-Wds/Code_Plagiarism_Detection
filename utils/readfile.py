# -*- coding: utf-8 -*- 

import os
import subprocess
import logging
from utils.util import *
from utils.winnowing import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

file_handler = logging.FileHandler('readfile.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def read_file(f):
    num = 0
    # when use the command, one should change the path to file: google-java-format-1.6-all-deps.jar
    cmdCommand = "java -jar C:\\Users\\dingwang\\Downloads\\google-java-format-1.6-all-deps.jar %s" % f
    process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    code = str(output).split("\\n")
    code[0] = code[0][2:]
    depth = depth_cal(code)
    test = polish(code)
    logger.debug("".join(test))
    w = winnow(test)
    return w
    # if depth < 5:
    #     return 0
    # else:
    #     test = polish(code)
    #     logger.debug("".join(test))
    #     w = winnow(test)
    #     return w


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
        elif ".groovy" in str(files):
            pass
        elif ".java" in str(files):
            if "test" in str(files) or "Test" in str(files) or "test" in str(root) or "Test" in str(root):
                pass
            else:
                for i in files:
                    f = open(root + "\\" + i, encoding="utf8")
                    a = f.read()
                    if "interface" in a:
                        pass
                    elif "abstract class" in a and not "return" in a:
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
