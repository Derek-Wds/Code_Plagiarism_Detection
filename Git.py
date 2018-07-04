import os, subprocess, logging, csv, shutil, sys, hashlib
from git import *
from utils.util import *
from utils.readfile import get_file
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


if __name__ == "__main__":

	# get the files that needed
	all_files = []
	all_commits = get_commits(repo, repo.references)
	csv_reader = csv.reader(open('data\\git\\git.csv', encoding='utf-8'))
	for row in csv_reader:
		all_files.extend(row)

	# get all the commits and store the corresponding winnows
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
					write_csv([f, commit, rf], "data\\git\\git_winnows.csv")
					logger.info(file)
				else:
					pass
		print(i)


	# get all the winnows into elastic search and search for the clones






	# get all the simhashes of the file and es insert and search


	