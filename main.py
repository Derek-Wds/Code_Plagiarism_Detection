from utils.util import polish
from utils.winnowing import winnow, select_min
from utils.resemblence import resemblence
from utils.writecsv import write_csv
from utils.readfile import get_file, read_file
from utils.elastic_search import search, insert
from pprint import pprint
import csv, json, sys, logging
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

file_handler = logging.FileHandler('main.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def main():
    # file1 = open('codes/data1.java','r')
    # file2 = open('codes/data2.java','r')
    # code1 = file1.read()
    # code2 = file2.read()

    # test1 = polish(code1)
    # test2 = polish(code2)

    # print(test1)

    # winnow1 = winnow(test1)
    # winnow2 = winnow(test2)


    # print(len(winnow1))
    # print(len(winnow2))
    # print(len(winnow1.intersection(winnow2)))

    # plt.figure("similarities")
    # data = []
    # labels = []
    # for i in range(1, 1000):
    #     #  resembelence(a, b, num_of_data_to_choose_in_a_and_b)
    #     data.append(resemblence(winnow1, winnow2, i))
    #     labels.append(i)
    # data = np.array(data)
    # labels = np.array(labels)
    # plt.plot(labels, data)
    # plt.show()

    # length1 = len(winnow1)
    # length2 = len(winnow2)

    # print("Similarity between two files are: ", resemblence(winnow1, winnow2, int((length1 + length2)/25)))
    
    # file_dic = {}
    # num = 1
    # files = get_file("C:\\Users\\dingwang\\Desktop\\guava-master")
    # for i in files:
    #     for j in range(len(files[i]["files"])):
    #         file_dic[num] = str(files[i]["root"] + "\\" + files[i]["files"][j])
    #         num += 1
    
    # winnows = {}
    # for i in file_dic:
    #     temp = [file_dic[i], read_file(file_dic[i])]
    #     # print(read_file(file_dic[i]))
    #     winnows[i] = temp
    #     write_csv(temp)
    #     print(i)

    winnows = {}
    num = 1
    csv_reader = csv.reader(open('data\\hash.csv', encoding='utf-8'))
    for row in csv_reader:
        winnows[num] = [row[0], eval(row[1])]
        # insert([num, row[0], row[1]])
        num += 1

    # results = {}
    # num = 1
    # for i in range(1, len(winnows)):
    #     for j in range(i + 1, len(winnows) + 1):
    #         result = resemblence(winnows[i][1], winnows[j][1], 500)
    #         logger.info([i, j, winnows[i][0], winnows[j][0], result])
    #         if result > 0.6:
    #             results[num] =  [i, j, winnows[i][0], winnows[j][0], result]
    #             num += 1

    # with open('data\\result.json', 'w') as f:
    #     json.dump(results, f)
    
    # with open('data\\result.json', 'r') as f:
    #     a = json.load(f)

    # for i in a:
    #     pprint(a[i])

if __name__ == "__main__":
    csv.field_size_limit(sys.maxsize)
    main()