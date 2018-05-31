from utils import *
from winnowing import *

def main():
    file1 = open('codes/AVLNode.java','r')
    file2 = open('codes/BSTNode.java','r')
    code1 = file1.read()
    code2 = file2.read()

    test1 = polish(code1)
    test2 = polish(code2)

    result1 = winnow(test1)
    result2 = winnow(test2)
    same = result1 & result2

if __name__ == "__main__":
    main()