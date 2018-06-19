from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from pprint import pprint

es = Elasticsearch([])
index_name = ["winnows"]
s = Search(using = es, index = index_name)

# query_all = {
#     'query': {
#         'match_all': {}
#     }
# }

# query_target = {
# 	'query': {
# 		'match': {
# 			'fields': 'data'
# 		}
# 	}
# }


# return a dictionary, each contains the two files and the match scores out of elasticsearch
# data is a list with data[0] is the file path, data[1] is the string of winnow values
def search(data):

	# res = es.search(index = index_name, body = query_all, timeout = 10)
	# pprint(res)

	w = sorted(eval(data[1]))
	res = {}
	shoulds = []
	
	for i in w:
		shoulds.append(Q({"match": {"winnow{}".format(i[0] + 1): str(i[1])}}))

	q = Q('bool', must = [], should = shoulds, minimum_should_match = "80%")
	result = s.query(q).execute()

	try:
		a = result[0]
		res[0] = [data[0], a.file, a.meta.score] # a.field
	except Exception as e:
		print("There is no match found!")
	else:
		try:
			a = result[1]
			res[1] = [data[0], a.file, a.meta.score] # a.field
		except:
			print("Done.")
		else:
			try:
				a = result[2]
				res[2] = [data[0], a.file, a.meta.score] # a.field
			except:
				print("Done.")
	return res


# data is list with first place be the id number, second be the file name, third one be a dictionary of winnow value
def insert(data):
	dic = data[2]
	body = {'file': data[1]}
	for i in dic:
		if i + 1 > 500:
			break
		body['winnow{}'.format(i+1)] = str(dic[i])
	es.index(index = index_name, doc_type = "code", body = body, id = data[0])


# for i in range(1, 11):
# 	print(es.get(index = index_name, doc_type='code', id = i))


# for i in range(1, 4504):
# 	es.delete(index = index_name, doc_type = "code", id = i)

# body = {'file': "test"}
# for i in range(1, 501):
# 	body['winnow{}'.format(i)] = 'a'
# es.index(index = index_name, doc_type = "code", body = body, id = 1)

# for i in range(1, 4504):
# 	es.delete(index = index_name, doc_type = "code", id = i)


a = ['C:\\Users\\dingwang\\Desktop\\elasticsearch-master\\x-pack\\plugin\\sql\\src\\main\\java\\org\\elasticsearch\\xpack\\sql\\expression\\function\\scalar\\math\\Sinh.java',"{(53, 143419550207688339278086857251512886511589384492), (15, 363838513602832068498342337483696424745087800887), (32, 230150865312966926446845921882505457120740863085), (22, 77556986765758119700675650966412165403797892978), (14, 230150865312966926446845921882505457120740863085), (29, 77556986765758119700675650966412165403797892978), (7, 685051054235258816562514159570242773345511775371), (57, 160369097502873397844910855466515689493888157278), (20, 724614941973376369510252595352924037788272495210), (25, 230150865312966926446845921882505457120740863085), (37, 552374789355930004349035398311116182420952821239), (11, 77556986765758119700675650966412165403797892978), (43, 219656753174819715989546651213032589448885952107), (36, 204092522699584814582865240355187914163760707630), (68, 306085206711865957936688847238131755471400717307), (10, 347833413078575421241989891353484715325316187259), (63, 34002671110405643084860825207073037316811538197), (48, 86385141035459989678315592807794322521456884109), (42, 572159204316997624157090687069138674523167837408), (59, 32168830112641786592524745520918902867451208640), (21, 347833413078575421241989891353484715325316187259), (72, 371210313578556255895395050081222007077795685999), (3, 329773855636074258335320143423211918623040726977)}"]
pprint(search(a))


# a = []
# for i in range(1, 501):
# 	a.append('Q("match", winnow{} = data[1][{}])'.format(i, i))
# print(a)