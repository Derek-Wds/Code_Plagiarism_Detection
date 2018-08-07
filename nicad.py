import os, subprocess, logging, csv, shutil, sys, hashlib, json, math, re
import numpy as np
from nicad_utils import *
from utils.util import *
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

file_handler = logging.FileHandler('data\\nicad\\nicad_info.log', encoding='utf-8')
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


# this method concot the hashes of different functions to a string in the order of depth, and calculate the simhash
def addup_simhash(weighted_features, f=64):
    v = [0] * f
    masks = [1 << i for i in range(f)]
    weighted_features = sorted(weighted_features, key = lambda x: int(x[1]))
    temp = []
    for ff in weighted_features:
        temp.append(ff[0])
    features = [''.join(temp)]
    for feature in features:
        h = _hash(feature)
        # weight = int(feature[1])
        weight = 1
        for i in range(f):
            v[i] = v[i] + weight if h & masks[i] else v[i] - weight
    value = 0
    for i in range(f):
        if v[i] > 0:
            value |= masks[i]
    return np.int64(np.uint64(value)).item()







# ---------------------break line-------------------------


if __name__ == "__main__":

    # split_xml()

    # seven_gram()

    with open('data\\nicad\\functions.json', 'r', encoding='utf-8') as f:
        dic = json.load(fp = f)

    with open('data\\nicad\\7-gram.json', 'r', encoding='utf-8') as f:
        dicts = json.load(fp = f)

    simhash_result = {}
    for file in dic:
        simhashes = []
        for function in dic[file]:
            logger.info([file, function, generate_features(dic[file][function])])
            print(file)
            print(function)
            print(dic[file][function])
            # print(generate_features(dic[file][function]))
            simhashes.append([str(calculate_simhash('|-|'.join(generate_features(dic[file][function])), dicts)[0]), 1])
        logger.info([file, simhashes])
        result = addup_simhash(simhashes)
        simhash_result[file] = result

    with open('data\\nicad\\simhash.json', 'w') as f:
        json.dump(simhash_result, f)

    with open('data\\nicad\\simhash.json', 'r') as f:
        simhashes = json.load(fp=f)

    id = 1
    for file in simhashes:
        print(id)
        hashval = simhashes[file]
        commit = file.split('-')[1][:-5]
        f = (file.split('-')[0]).split("\\")[-1] + '.java'
        body = {'file': f, 'commit': commit, "hashval": hashval}
        es.index(index = ["nicad_simhashes"], doc_type = "simhashes", body = body, id = id)
        id += 1


    # matches = get_all_matches("nicad_simhashes")
    # with open('data\\nicad\\result.json', 'r') as f:
    #     dic = json.load(fp = f)
    # total_matches = 0
    # for i in matches:
    #     total_matches += len(matches[i]) - 1
    # print("total matches: ", total_matches)
    # test_matches = 0
    # wrong_matches = 0
    # s = Search(using = es, index = "nicad_simhashes")[0:50]
    # for i in dic['true']:
    #     f = es.get(index='nicad_simhashes', id='{}'.format(int(i)))['_source']
    #     file = f['file'][:-5] + '-' + f['commit'] + '.java'
    #     for num in dic['true'][i]:
    #         if int(i) in matches[file]:
    #             if num in matches[file]:
    #                 test_matches += 1
    #             else:
    #                 wrong_matches += 1
    # for i in dic['false']:
    #     wrong_matches += len(dic['false'][i])
    # print("test matches: ", test_matches)
    # print("wrong matches: ", wrong_matches)
    # print("Ratio: ", test_matches / total_matches) # Ratio:  0.6960288189381594
    # print("Accuracy based on found: ", test_matches/(test_matches + wrong_matches))



# '''
#     Use only idf:

#     total matches:  46636
#     test matches:  30188
#     wrong matches:  222
#     Ratio:  0.6473110901449524
#     Accuracy based on found:  0.9926997698125617

#     Use idf + function depth:

#     total matches:  46636
#     test matches:  29015
#     wrong matches:  98
#     Ratio:  0.6221588472424736
#     Accuracy based on found:  0.9966338062034142
# '''


# # Test with function wise duplicate
#     with open('data\\nicad\\functions.json', 'r') as f:
#         dic = json.load(fp = f)

#     with open('data\\nicad\\7-gram.json', 'r') as f:
#         dicts = json.load(fp = f)

#     function_simhash = {}
#     s = []
#     for file in dic:
#         for function in dic[file]:
#             depth = depth_cal(dic[file][function])
#             if depth >= 5:
#                 simhash = str(calculate_simhash('|-|'.join(generate_features(dic[file][function])), dicts)[0])
#                 s.append(simhash)
#     for i in s:
#         function_simhash[i] =[]

#     for file in dic:
#         simhashes = []
#         for function in dic[file]:
#             logger.info([file, function, generate_features(dic[file][function])])
#             depth = depth_cal(dic[file][function])
#             if depth >= 5:
#                 simhash = str(calculate_simhash('|-|'.join(generate_features(dic[file][function])), dicts)[0])
#                 simhashes.append(simhash)
#                 for i in function_simhash:
#                     if distance(i, simhash) <= 3:
#                         function_simhash[i].append([file, function])

#     with open('data\\nicad\\function_simhash.json', 'w') as f:
#         json.dump(function_simhash, f)


#     a = '|-|'.join(generate_features(dic["data/src/GeoPointFieldMapper-86c47b27a86888428c282839d8b6bcb602452d52.java"]["function19"]))
#     # print(a)
#     print(calculate_simhash(a, dicts)[1])
#     print()
#     b = '|-|'.join(generate_features(dic["data/src/GeoPointFieldMapper-31aabe4bf9ea73cbb1c21322d9e9aa2a578b41a0.java"]["function21"]))
#     # print(a)
#     print(calculate_simhash(b, dicts)[1])


#     pprint(calculate_simhash('|-|'.join(generate_features(dic["data/src/GeoPointFieldMapper-86c47b27a86888428c282839d8b6bcb602452d52.java"]["function19"])), dicts)[1])
#     print()
#     pprint(calculate_simhash('|-|'.join(generate_features(dic["data/src/GeoPointFieldMapper-31aabe4bf9ea73cbb1c21322d9e9aa2a578b41a0.java"]["function21"])), dicts)[1])
#     print(distance("3466988347902415211", "4701470302343188542"))

