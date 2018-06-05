from utils import polish, read_file
from winnowing import winnow, select_min
from resemblence import resemblence
import numpy as np
from readfile import get_file
import matplotlib as mpl
import matplotlib.pyplot as plt

def main():
    # file1 = open('codes/data1.java','r')
    # file2 = open('codes/data2.java','r')
    # code1 = file1.read()
    # code2 = file2.read()

    # test1 = polish(code1)
    # test2 = polish(code2)

    # # print(test1)

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
    
    file_dic = {}
    num = 1
    files = get_file("C:\\Users\\dingwang\\Desktop\\Java-master")
    for i in files:
        for j in range(len(files[i]["files"])):
            file_dic[num] = str(files[i]["root"] + "\\" + files[i]["files"][j])
            num += 1

    winnows = {}
    for i in file_dic:
        print(i)
        winnows[file_dic[i]] = read_file(file_dic[i])

    print(winnows)


    

    



if __name__ == "__main__":
    main()