import string
import json

global class_name
class_name = []
global func_name
func_name = []


def punc_del(code):
    original_list = code.split()
    temp_code = ''.join(original_list)
    char_list = []
    for i in temp_code:
        if i not in string.punctuation:
            char_list.append(i)
    return ''.join(char_list)


def cf_change(code_list):
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
                if char != "(" and char != "<":
                    temp.append(char)
                else:
                    break
            name = ''.join(temp)
            if name not in func_name and name not in class_name:
                func_name.append(''.join(temp))
            code_list[i] = 'F'
    return code_list


def val_change(code_list):
    with open('conf/java.json', 'r') as f:
        common = json.load(f)
    temp = []
    for i in code_list:
        temp.append(' ')
        for j in range(len(i)):
            if i[j] in string.punctuation:
                if i[j] == '_':
                    temp.append('_')
                else:
                    temp.append(' ')
            else:
                temp.append(i[j])
    code_list = (''.join(temp)).split()
    for name in range(len(code_list)):
        if code_list[name] in class_name:
            code_list[name] = "C"
        elif code_list[name] in func_name:
            code_list[name] = "F"
        else:
            if code_list[name] not in common['code']:
                if code_list[name].isnumeric():
                    pass
                else:
                    code_list[name] = "V"
    return code_list


def comment_del(code_list):
    pos = 0
    while pos != len(code_list):
        if code_list[pos] == "/*" or code_list[pos] == "/**":
            while code_list[pos] != "*/":
                code_list[pos] = ''
                pos += 1
        elif code_list[pos] == "*/":
            code_list[pos] = ''
            pos += 1
        else:
            pos += 1
    return code_list


def polish(code):
    original_list = code.lower().split()
    result = val_change(cf_change(comment_del(original_list)))
    return ''.join(result)
