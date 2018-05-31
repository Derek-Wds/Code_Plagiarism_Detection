from utils import polish
from winnowing import winnow, select_min
import numpy as np

def main():
    file1 = open('codes/AVLNode.java','r')
    file2 = open('codes/BSTNode.java','r')
    code1 = file1.read()
    code2 = file2.read()

    test1 = polish(code1)
    test2 = polish(code2)

    winnow1 = winnow(test1)
    winnow2 = winnow(test2)

    # 300 is just a test number, can change
    list1 = sorted(list(winnow1))[:300]
    list2 = sorted(list(winnow2))[:300]
    
    w1 = set(list1)
    w2 = set(list2)
    w12 = set(sorted(list(w1.union(w2))[:300]))

    resemble = len(w1.intersection(w2).intersection(w12)) / len(w12)
    print(resemble)
if __name__ == "__main__":
    main()