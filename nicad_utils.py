import os, subprocess, logging, csv, shutil, sys, hashlib, json, math, re
import numpy as np
from utils.util import *
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

file_handler = logging.FileHandler('data\\nicad\\nicad_utils_info.log', encoding='utf-8')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# elasticsearch
es = Elasticsearch([{'host':'icam-prod-ms-20','port':9200}])


# xml file source
# xml_file = "data\\nicad\\_functions-consistent.xml"
xml_file = "data\\nicad\\src_functions-consistent.xml"


# ---------------------break line-------------------------


# TODO: a better hash function
# this one returns 128 bit int, more than 64.
def _hash(x):
    return int(hashlib.md5(x.encode("utf-8")).hexdigest(), 16)



def calculate_simhash(weighted_features, dicts, f=64):
    grams = {}
    v = [0] * f
    masks = [1 << i for i in range(f)]
    features = weighted_features.split("|-|")
    for feature in features:
        # tf = features.count(feature)
        idf = math.log(33867/dicts[feature]['num_of_file'], 2)
        # idf = 1
        weight = idf
        grams[feature] = idf
        h = _hash(feature)
        for i in range(f):
            v[i] = v[i] + weight if h & masks[i] else v[i] - weight
    value = 0
    for i in range(f):
        if v[i] > 0:
            value |= masks[i]
    return np.int64(np.uint64(value)).item(), grams


def add_simhash(weighted_features, f=64):
    v = [0] * f
    masks = [1 << i for i in range(f)]
    for feature in weighted_features:
        h = int(feature[0])
        # weight = int(feature[1])
        weight = 1
        for i in range(f):
            v[i] = v[i] + weight if h & masks[i] else v[i] - weight
    value = 0
    for i in range(f):
        if v[i] > 0:
            value |= masks[i]
    return np.int64(np.uint64(value)).item()


# get all the tokens of a function and combine them into a sting. store thme into a list
def generate_features(lines):
    function = ''
    for line in lines:
        function += line
    tokens = function.split()
    length = len(tokens)
    result = []
    if length < 7:
        string = ''
        for i in range(len(tokens)):
            if i != len(tokens) - 1:
                string = string + tokens[i] + " "
            else:
                string = string + tokens[i]
        result.append(string)
    else:
        for i in range(length - 7 + 1):
            string = ''
            for token in tokens[i:i+7]:
                string = string + token + " "
            string = string[:-1]
            result.append(string)
    return result


def get_all_matches(idx):
    output = {}
    with open('data\\nicad\\simhash.json', 'r', encoding='utf-8') as f:
        all_files = json.load(fp=f)
    s = Search(using = es, index = "nicad_simhashes")[0:50]
    for i in all_files:
        file = (i.split('-')[0]).split("/")[-1] + '.java'
        output[i] = []
        res = s.query("match", file="{}".format(file)).execute()
        for j in res:
            if word_bags(i, j.file[:-5] + '-' + j.commit + '.java'):
                output[i].append(int(j.meta.id))
                output[i].sort()
        print(i)
    return output


def word_bags(a, b):
    f1 = "C:\\Users\\dingwang\\Desktop\\"+a.replace('/','\\')
    f2 = "C:\\Users\\dingwang\\Desktop\\"+b.replace('/','\\')
    bags1 = collect_words(f1, open(f1, 'r', encoding='utf-8').read())
    bags2 = collect_words(f2, open(f2, 'r', encoding='utf-8').read())
    count = 0
    length1 = 0
    length2 = 0
    for i in bags1:
        length1 += bags1[i]
    for i in bags2:
        length2 += bags2[i]
    if (length1 - length2) / length2 > 0.1 or (length2 - length1) / length1 > 0.1:
        logger.debug('situation 1')
        return False
    else:
        if len(bags1) >= len(bags2):
            for i in bags2:
                if count / len(bags2) >= 0.1:
                    logger.debug('situation 2')
                    return False
                try:
                    if bags2[i] >= bags1[i]:
                        if (bags2[i] - bags1[i])/bags2[i] > 0.5:
                            logger.debug('situation 3')
                            return False
                    else:
                         if (bags1[i] - bags2[i])/bags1[i] > 0.5:
                            logger.debug('situation 4')
                            return False
                except:
                    count += 1
        else:
            for i in bags1:
                if count / len(bags1) >= 0.1:
                    logger.debug('situation 5')
                    return False
                try:
                    if bags2[i] >= bags1[i]:
                        if (bags2[i] - bags1[i])/bags2[i] > 0.5:
                            logger.debug('situation 6')
                            return False
                    else:
                         if (bags1[i] - bags2[i])/bags1[i] > 0.5:
                            logger.debug('situation 7')
                            return False
                except:
                    count += 1
    return True


def collect_words(F, f):
    bags = {}
    file, cn = comment_del(f.split('\n'))
    words = re.findall(r"[\w']+", ''.join(file))
    for word in words:
        if word == '':
            pass
        else:
            try:
                bags[word] += 1
            except:
                bags[word] = 1
    logger.info([F, bags])
    return bags




def distance(a, b):
    a = int(a)
    b = int(b)
    return bin(a ^ b).count('1')


# ---------------------break line-------------------------

# delete the generics in each line.
def delete_generics(line):
    temp = []
    count = 0
    if "<" in line and ">" in line:
        for w in line:
            if w != "<" and count == 0:
                temp.append(w)
            elif w == "<":
                count += 1
            elif w == ">":
                count -= 1
            else:
                pass
        return "".join(temp)

    else:
        return line



# deal with the xml data, per function.
def split_xml():
    result = {}
    xml_content = open(xml_file, 'r', encoding='utf-8').readlines()
    num = 0
    for line in xml_content:
        if "<source file=" in line:
            file = line.split()[1][6:-1]
            num += 1
        elif "</source>" not in line:
            line = delete_generics(line)
            try:
                result[file]['function{}'.format(num)].append(line)
            except:
                if file in result:
                    try:
                        result[file]['function{}'.format(num)].append(line)
                    except:
                        result[file]['function{}'.format(num)] = [line]
                else:
                    num = 1
                    result[file] = {}
                    result[file]['function{}'.format(num)] = [line]
        else:
            pass

    with open('data\\nicad\\functions.json', 'w', encoding='utf-8') as f:
        json.dump(result, f)



# ---------------------break line-------------------------

def seven_gram():
    grams = {}
    with open('data\\nicad\\functions.json', 'r', encoding='utf-8') as f:
        dic = json.load(fp = f)
    for file in dic:
        all_grams = []
        for function in dic[file]:
            function_grams = generate_features(dic[file][function])
            all_grams.extend(function_grams)
            for gram in function_grams:
                try:
                    grams[gram]['total_num'] += 1
                except:
                    grams[gram] = {'total_num':1, "num_of_file":0}
        all_grams = list(set(all_grams))
        for gram in all_grams:
            grams[gram]['num_of_file'] += 1
    with open('data\\nicad\\7-gram.json', 'w', encoding='utf-8') as f:
        json.dump(grams, f)


