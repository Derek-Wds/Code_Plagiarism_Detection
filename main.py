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
    files = get_file("C:\\Users\\dingwang\\Desktop\\guava-master")
    for i in files:
        for j in range(len(files[i]["files"])):
            file_dic[num] = str(files[i]["root"] + "\\" + files[i]["files"][j])
            num += 1

    winnows = {}
    for i in file_dic:
        winnows[i] = [file_dic[i], read_file(file_dic[i])]

    
    results = {}
    num = 1
    for i in range(1, len(winnows)):
        for j in range(i + 1, len(winnows) + 1):
            result = resemblence(winnows[i][1], winnows[j][1], 500)
            if result > 0.6:
                results[num] =  [winnows[i][0], winnows[j][0], result]
                num += 1

    for i in results:
        print(results[i])

    # a = read_file("C:\\Users\\dingwang\\Desktop\\guava-master\\android\\guava\\src\\com\\google\\common\\io\\LineReader.java")
    # print("\n")
    # b = read_file("C:\\Users\\dingwang\\Desktop\\guava-master\\guava\\src\\com\\google\\common\\io\\LineReader.java")
    # print("\n")
    # print(len(a))
    # print("\n")
    # print(len(b))
    # print(a.intersection(b))
    # print("\n")
    # print(len(a.intersection(b)))
    # print(resemblence(a, b, 500))

if __name__ == "__main__":
    main()