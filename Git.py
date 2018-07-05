import os, subprocess, logging, csv, shutil, sys, hashlib, json
import numpy as np
from git import *
from utils.util import *
from utils.winnowing import *
from utils.writecsv import write_csv
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


global GIT_REPO_PATH, repo
GIT_REPO_PATH = "C:\\Users\\dingwang\\Desktop\\elasticsearch"
repo = Repo(GIT_REPO_PATH, odbt = GitCmdObjectDB)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

file_handler = logging.FileHandler('data\\git\\git_info.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

es = Elasticsearch([{'host':'icam-prod-ms-20','port':9200}])

# get all the java file in the projects that have depth >= 5 and store them into data\\git\\git.csv
def file_filter():
	files = get_file(GIT_REPO_PATH)
	outputs = []
	for num in files:
		print(num)
		for file in files[num]['files']:
			f = files[num]['root'] + '\\' + file
			cmdCommand = "java -jar C:\\Users\\dingwang\\Downloads\\google-java-format-1.6-all-deps.jar %s" % f
			process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
			output, error = process.communicate()
			code = str(output).split("\\n")
			code[0] = code[0][2:]
			depth = depth_cal(code)
			if depth >= 5:
				outputs.append(f)
				write_csv([f],'C:\\Users\\dingwang\\Desktop\\Code_detect\\data\\git\\git.csv')
	return outputs



def get_commits(repo, ref_name):
    commits = []
    for commit in repo.iter_commits(rev = ref_name):
        commits.append(str(commit))
    return commits



def get_diff_files(commit1, commit2):
	diff = repo.git.diff(commit1, commit2)
	smalls = diff.split("\n")
	length = len(smalls)
	java_files = {commit1:[], commit2:[]}
	for num in range(length - 1):
		a = smalls[num].replace('/', '\\')
		b = smalls[num + 1].replace('/', '\\')
		if "---" in a and "+++" in b:
			if "/dev/null" in a or "/dev/null" in b:
				pass
			else:
				if ".java" in a and ".java" in b:
					java_files[commit1].append(GIT_REPO_PATH + a[5:])
					java_files[commit2].append(GIT_REPO_PATH + b[5:])
					# should store .java and move them to the right place
	return java_files



# file should be a tuple that (a,b), a: file name, b: commit hash
def checkout_file(file):
	repo.git.checkout(file[1], file[0])
	return file


# move the file to the directory data on desktop
# NOTE: oldname should be a tuple that (a,b), a: file name, b: commit hash
def move_file(oldname):
	compos = oldname[0].split("\\")[-1].split(".")
	aa, bb = compos[0], compos[1]
	newname = "C:\\Users\\dingwang\\Desktop\\data\\" + aa + "-" + str(oldname[1]) + "." + bb
	shutil.copyfile(oldname[0], newname)


def readfile(file):
	output = str(open(file, encoding='utf-8').read())
	code = output.split("\n")
	test = polish(code)
	logger.debug("".join(test))
	w = winnow(test)
	return w

def getfile(path):
	file_dic = {}
	num = 1
	for root, dirs, files in os.walk(path):
		if files is None:
			pass
		else:
			for i in files:
				f = root + "\\" + i
				file_dic[num] = f
				num += 1
	return file_dic





# ---------------------break line-------------------------






# data should be one row in the git_winnows.csv
def insert(data):
	file_name, file_commit = data[1], data[2]
	winnows = sorted(eval(data[3]))
	winnow_dic = {}
	for t in winnows:
		winnow_dic[t[0]] = t[1]
	body = {"file": file_name, "commit":file_commit}
	for i in winnow_dic:
		if i + 1 > 500:
			break
		body['winnow{}'.format(i+1)] = str(winnow_dic[i])
	es.index(index = ["git_winnows"], doc_type = "winnows", body = body, id = data[0])


# Return a dictionary that contains the clones with their ids
# input data should be a line of the file git_winnows.csv
def search(data):
	w = sorted(eval(data[3]))
	res = {}
	shoulds = []
	for i in w:
		if i[0] > 499:
			break
		shoulds.append(Q({"match": {"winnow{}".format(i[0] + 1): str(i[1])}}))
	q = Q('bool', must = [], should = shoulds, minimum_should_match = "80%")
	s = Search(using = es, index = ["git_winnows"])[0:50]
	result = s.query(q).execute()
	file = data[1][:-5] + "-" + data[2] + ".java"
	res[file] = []
	if result is None:
		pass
	else:
		for i in result:
			res[file].append((i.file, i.meta.id, i.commit))
	return res





# ---------------------break line-------------------------





# TODO: a better hash function
# this one returns 128 bit int, more than 64.
def _hash(x):
    return int(hashlib.md5(x.encode("utf-8")).hexdigest(), 16)



def calculate_simhash(weighted_features, f=64):
    v = [0] * f
    masks = [1 << i for i in range(f)]
    weight = 1
    features = weighted_features.split()
    for feature in features:
        h = _hash(feature)
        for i in range(f):
            v[i] = v[i] + weight if h & masks[i] else v[i] - weight
    value = 0
    for i in range(f):
        if v[i] > 0:
            value |= masks[i]
    return np.int64(np.uint64(value)).item()


# 
def get_all_winnows(file, id):
	result = []
	w = readfile(file)
	for h in range(len(w)):
		if h == len(w) - 1:
			for j in w[h]:
				result.append(str(j[1]))
		else:
			result.append(str(w[h][0][1]))
	fingerprint = ' '.join(result)
	write_csv([id, file, fingerprint], 'data\\git\\git_simhash.csv')
	logger.info([id, file, fingerprint])
	print(i)


# this function collects all the winnow values and store them in a json file
def collect_winnows():
	w = []
	ws = {}
	num = 1
	csv_reader = csv.reader(open('data\\git\\git_simhash.csv', encoding='utf-8'))
	for row in csv_reader:
		print(num)
		W = row[2].split()
		for i in W:
			w.append(eval(i))
			try:
				ws[eval(i)][0] += 1
			except:
				ws[eval(i)] = [1,0]
		W = set(W)
		for i in W:
			ws[eval(i)][1] += 1
		num += 1

	print()
	print("done")
	print()
	print(len(w))
	print(len(set(w)))

	a = sorted(ws.items(), key = lambda item: item[1][1])
	n50 = 0
	n100 = 0
	for i in a:
		if i[1][1] < 50:
			n50 += 1
		if i[1][1] < 100:
			n100 += 1
	print()
	print("50: ", n50/len(set(w)))
	print("100: ", n100/len(set(w)))

	# with open('data\\git\\simhashes_result.json', 'w') as f:
	# 	json.dump(ws, f)




# ---------------------break line-------------------------




# gather all the datas
def gather_data():
	# get the files that needed
	all_files = []
	all_commits = get_commits(repo, repo.references)
	csv_reader = csv.reader(open('data\\git\\git.csv', encoding='utf-8'))
	for row in csv_reader:
		all_files.extend(row)

	# get all the commits and store the corresponding winnows
	num = 1
	for i in range(20): # len(all_commits) - 1
		commit1 = all_commits[i]
		commit2 = all_commits[i + 1]

		files = get_diff_files(commit1, commit2)
		for commit in files:
			for f in files[commit]:
				file = (f, commit)
				if f in all_files:
					rf = readfile(f)
					move_file(checkout_file(file))
					write_csv([num, f, commit, rf], "data\\git\\git_winnows.csv")
					logger.info(file)
					num += 1
				else:
					pass
		print(i)





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

# winnows
	# # get all the winnows into elastic search and search for the clones
	# csv_reader = csv.reader(open('data\\git\\git_winnows.csv', encoding='utf-8'))
	# for row in csv_reader:
	# 	insert(row)
	# 	print(row[0])

	# f = open("data\\git\\winnows_result.json", "w")
	# csv_reader1 = csv.reader(open('data\\git\\git_winnows.csv', encoding='utf-8'))
	# result = {}
	# for row in csv_reader1:
	# 	res = search(row)
	# 	result[row[0]] = res
	# 	print(row[0])
	# 	if eval(row[0]) == 200:
	# 		break
	# json.dump(result, f)
	# f.close()



# simhash
	# get all the simhashes of the file and es insert and search
	# all_files = getfile("C:\\Users\\dingwang\\Desktop\\data")
	# for i in all_files:
	# 	get_all_winnows(all_files[i], i)

	# collect_winnows()

	# winnows showed up times: ( 50:  0.8469644643836943 / 100:  0.9221831326856663 )
	# winnows showed up in the file numbers: ( 50:  0.8831940096181777 / 100:  0.9457040957944679 )

	csv_reader1 = csv.reader(open('data\\git\\git_simhash.csv', encoding='utf-8'))
	with open('data\\git\\simhashes_result.json', 'r') as f:
		dic = json.load(fp = f)

	for row in csv_reader1:
		print(row[0])
		file = row[1].split("-")[0] + ".java"
		commit = row[1].split("-")[1][:-5] 
		ws = row[2].split()
		temp = []
		for w in ws:
			if dic[w][1] > 50:
				pass
			else:
				temp.append(w)

		fingerprint = calculate_simhash(' '.join(temp))
		es.index(index = "git_simhashes", doc_type = "simhashes", body = {"hashval": fingerprint, "file": file, "commit": commit}, id = row[0])


