# python file for noise filter

import string
import json
from winnowing import winnow, select_min

#delete punctuations
def punc_del(code_list):
    temp = []
    flag = 0
    for i in code_list:
        if "@" in i:
            temp.append('')
        else:
            temp.append(' ')
            for j in range(len(i)):
                if flag == 1:
                    if i[j] == "'" or i[j] == '"':
                        temp.append("V")
                        flag = 0
                    continue
                else:
                    if i[j] in string.punctuation:
                        if i[j] == '_':
                            temp.append('_')
                        else:
                            if i[j] == '"' or i[j] == "'":
                                flag = 1
                            else:
                                temp.append(' ')
                    else:
                        temp.append(i[j])
    code_list = (''.join(temp)).split()
    return code_list

#change class name and function name
def cf_change(code_list):
    class_name = []
    func_name = []
    for i in range(len(code_list)):
        # change class name
        if code_list[i] == "class" or code_list[i] == "extends":
            temp = []
            for char in code_list[i+1]:
                if char != "<":
                    temp.append(char)
                else:
                    break
            class_name.append(''.join(temp))
        
        # change funtion name
        if "(" in code_list[i] and "." not in code_list[i] and code_list[i][0] != "(":
            temp = []
            for char in code_list[i]:
                if char != "(" and char != "<" and char != "{":
                    temp.append(char)
                else:
                    break
            name = ''.join(temp)
            if name not in func_name and name not in class_name:
                func_name.append(''.join(temp))
        
        if "." in code_list[i] and "(" in code_list[i]:
            temp = []
            pos = 0
            while True:
                if code_list[i][pos] != ".":
                    pos += 1
                else:
                    pos += 1
                    break
            while code_list[i][pos] != "(":
                temp.append(code_list[i][pos])
                pos += 1
                if pos == len(code_list[i]):
                    break
            name = ''.join(temp)
            if name not in func_name and name not in class_name:
                func_name.append(''.join(temp))
                    
    return code_list, class_name, func_name


#change variable name and at the same time, change all the class name and function name
def val_change(code_list, class_name, func_name):
    with open('conf/java.json', 'r') as f:
        common = json.load(f)
    for i in range(len(code_list)):
        if "." not in code_list[i]:
            if code_list[i] in func_name or code_list[i][1:] in func_name:
                code_list[i] = "V"
    code_list = punc_del(code_list)
    for name in range(len(code_list)):
        if "exception" in code_list[name] or code_list[name] in common["code"]:
            continue
        elif code_list[name] in func_name:
            code_list[name] = "F"
        elif code_list[name] in class_name:
            code_list[name] = "C"
        else:
            if code_list[name].isdigit() or code_list[name].replace('.','',1).isdigit():
                code_list[name] = "N"
            else:
                code_list[name] = "V"
    return code_list

#delete comments
def comment_del(code_list):
    pos = 0
    run = True
    while run:
        if "/*" in code_list[pos]:
            while True:
                if "*/" in code_list[pos]:
                    code_list[pos] = ""
                    pos += 1
                    break
                code_list[pos] = ''
                pos += 1
        else:
            if "//" in code_list[pos]:
                num = code_list[pos].index("//")
                code_list[pos] = code_list[pos][:num]
            pos += 1
        if pos == len(code_list):
            run = False
            break    
        code_list[pos] += " "
    return ''.join(code_list).split()


# ---------------------break line-------------------------

#main function
def polish(code):
    del_com_list = comment_del(code)
    cf_replace, class_name, func_name = cf_change(del_com_list)
    result = val_change(cf_replace, class_name, func_name)
    return result
