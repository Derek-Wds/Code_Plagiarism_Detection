from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from pprint import pprint

es = Elasticsearch([""])
index_name = ["shakespeare"]
s = Search(using = es, index = index_name)

# query_all = {
#     'query': {
#         'match_all': {}
#     }
# }

# query_target = {
# 	'query': {
# 		'match': {
# 			'text_entry': 'But'
# 		}
# 	}
# }

def search(data):

	# res = es.search(index = index_name, body = query_all, timeout = 10)
	# pprint(res)
	res = {}
	result = s.query("match", text_entry = "{}".format(data[1])).execute()
	num = []
	for i in range(3):
		a = result[i]
		res[i] = [data[0], a.file, a.meta.score]
		print(a.meta.score, a.text_entry)
	return res


search(["hhh","but the"])