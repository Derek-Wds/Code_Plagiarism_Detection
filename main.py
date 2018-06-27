from utils.util import polish
from utils.winnowing import winnow, select_min
from utils.resemblence import resemblence
from utils.writecsv import write_csv
from utils.readfile import get_file, read_file
from utils.elastic_search import search, insert
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import csv, json, sys, logging, hashlib
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

file_handler = logging.FileHandler('main.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


es = Elasticsearch([{'host':'icam-prod-ms-20','port':9200}])

def main():
    
# # improvemed
    num = 0
    csv_reader = csv.reader(open('data\\test.csv', encoding='utf-8'))
    for row in csv_reader:
        print(num)
        write_csv([row[0], calculate_simhash(row[1])], 'data\\simhash.csv')
        num += 1
    csv_reader = csv.reader(open('data\\simhash.csv', encoding='utf-8'))
    id = 1
    for row in csv_reader:
        print(id)
        es.index(index = "simhashes", doc_type = "simhashes", body = {"hashval": eval(row[1]), "file": row[0]}, id = id)
        id += 1
 
# TODO: a better hash function
# this one returns 128 bit int, more than 64.
def _hash(x):
    return int(hashlib.md5(x.encode("utf-8")).hexdigest(), 16)



def calculate_simhash(weighted_features, f=64):
    v = [0] * f
    masks = [1 << i for i in range(f)]
    weight = 0
    features = weighted_features.split()
    length = len(features)
    for feature in features:
        h = _hash(feature)
        weight = weighted_features.count(feature) / length
        for i in range(f):
            v[i] = v[i] + weight if h & masks[i] else v[i] - weight
    value = 0
    for i in range(f):
        if v[i] > 0:
            value |= masks[i]
    return np.int64(np.uint64(value)).item()


def test1():
    file1 = open('codes/data1.java','r')
    file2 = open('codes/data2.java','r')
    code1 = file1.read()
    code2 = file2.read()

    test1 = polish(code1)
    test2 = polish(code2)

    print(test1)

    winnow1 = winnow(test1)
    winnow2 = winnow(test2)


    print(len(winnow1))
    print(len(winnow2))
    print(len(winnow1.intersection(winnow2)))

    plt.figure("similarities")
    data = []
    labels = []
    for i in range(1, 1000):
        #  resembelence(a, b, num_of_data_to_choose_in_a_and_b)
        data.append(resemblence(winnow1, winnow2, i))
        labels.append(i)
    data = np.array(data)
    labels = np.array(labels)
    plt.plot(labels, data)
    plt.show()

    length1 = len(winnow1)
    length2 = len(winnow2)

    print("Similarity between two files are: ", resemblence(winnow1, winnow2, int((length1 + length2)/25)))


def test2():
    file_dic = {}
    num = 1
    files = get_file("C:\\Users\\dingwang\\Desktop\\elasticsearch-master")
    for i in files:
        for j in range(len(files[i]["files"])):
            file_dic[num] = str(files[i]["root"] + "\\" + files[i]["files"][j])
            num += 1
    
    winnows = {}
    for i in file_dic:
        if read_file(file_dic[i]) == 0:
            pass
        else:
            temp = [file_dic[i], read_file(file_dic[i])]
            # print(read_file(file_dic[i]))
            winnows[i] = temp
            write_csv(temp, 'data\\hash.csv')
            print(i)

    winnows = {}
    num = 1
    csv_reader = csv.reader(open('data\\hash.csv', encoding='utf-8'))
    for row in csv_reader:
        winnows[num] = [row[0], eval(row[1])]
        a = sorted(eval(row[1]))
        w = {}
        for i in a:
            w[i[0]] = i[1]
        insert([num, row[0], w])
        print(num)
        num += 1


# O(n^2) time complexity
    results = {}
    num = 1
    for i in range(1, len(winnows)):
        for j in range(i + 1, len(winnows) + 1):
            result = resemblence(winnows[i][1], winnows[j][1], 500)
            logger.info([i, j, winnows[i][0], winnows[j][0], result])
            if result > 0.8:
                results[num] =  [i, j, winnows[i][0], winnows[j][0], result]
                print(num)
                num += 1

    with open('data\\result.json', 'w') as f:
        json.dump(results, f)
    
    with open('data\\result.json', 'r') as f:
        a = json.load(f)

    for i in a:
        pprint(a[i])



if __name__ == "__main__":
    # csv.field_size_limit(sys.maxsize)
    maxInt = sys.maxsize
    decrement = True

    while decrement:
        # decrease the maxInt value by factor 10 
        # as long as the OverflowError occurs.
        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt/10)
            decrement = True
    main()