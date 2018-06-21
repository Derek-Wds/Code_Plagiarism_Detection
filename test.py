import csv, sys, os, subprocess
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression  
from pprint import pprint
from utils.util import *
from utils.readfile import get_file

maxInt = sys.maxsize
decrement = True

while decrement:
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True


winnow_length = []
line_length = []
csv_reader = csv.reader(open('data\\hash.csv', encoding='utf-8'))
for row in csv_reader:
	file = open(row[0], encoding="utf8")
	line_length.append(len(file.readlines()))
	winnow_length.append(len(eval(row[1])))
x = np.array(line_length).reshape(-1, 1)
y = np.array(winnow_length).reshape(-1, 1)
LR = LinearRegression()
LR.fit(x, y)
print('intercept_:%.3f' % LR.intercept_)  
print('coef_:%.3f' % LR.coef_)  
plt.scatter(line_length, winnow_length,alpha=0.5,edgecolors= 'white')
plt.plot(x, LR.predict(x), color='red', linewidth=1)  
plt.grid(True)
plt.show()


# non_dup = 0
# dup = 0
# for row in csv_reader:
# 	dic = {}
# 	w = eval(row[1])
# 	for i in w:
# 		try:
# 			dic[i[1]] += 1
# 		except:
# 			dic[i[1]] = 1
# 	# l = sorted(dic.items(),key = lambda x:x[1],reverse = True)
# 	print(row[0])
# 	# for i in range(1):
# 	# 	print(l[i][0], l[i][1])
# 	non_dup += len(dic)
# 	dup += len(w)
# 	print(len(dic), len(w))
# print(non_dup/dup)




file_dic = {}
num = 1
files = get_file("C:\\Users\\dingwang\\Desktop\\elasticsearch-master")
for i in files:
	for j in range(len(files[i]["files"])):
		file_dic[num] = str(files[i]["root"] + "\\" + files[i]["files"][j])
		num += 1

brackets = {}

X=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
Y=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for i in file_dic:
	cmdCommand = "java -jar C:\\Users\\dingwang\\Downloads\\google-java-format-1.6-all-deps.jar %s" % file_dic[i]
	process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	code = str(output).split("\\n")
	code[0] = code[0][2:]
	del_com_list, cn = comment_del(code)
	code = ''.join(del_com_list)
	bracket = 0
	depth = 0
	for char in code:
		if char == "{":
			bracket += 1
		elif char == "}":
			bracket -= 1
		else:
			pass
		if bracket > depth:
			depth = bracket
	brackets[file_dic[i]] = depth
	Y[depth] += 1
	print(i)

pprint(brackets)
fig = plt.figure()
plt.bar(X,Y,0.4,color="blue")

plt.xlabel("depth")
plt.ylabel("numbers")
plt.title("bar chart")
for a,b in zip(X,Y):
	plt.text(a, b+0.01, '%.0f' % b, ha='center', va= 'bottom',fontsize=8)
plt.show() 
