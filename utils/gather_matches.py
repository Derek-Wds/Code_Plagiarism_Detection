import json
from elasticsearch import Elasticsearch


global es, matches
es = Elasticsearch()
matches = set()


def found(matches, lookup_id, match_id):
    if lookup_id < match_id:
        match = (lookup_id, match_id)
    else:
        match = (match_id, lookup_id)
    return match in matches


def parse_id(line):
    if line:
        parts = line.split(" ")
        if len(parts) == 2:
            return parts[1]
    return None


def fetch_es(doc_id):
    global es
    result = es.get(index='simhashes', doc_type='simhashes', id=doc_id)
    if result and result.get('_source'):
        return result
    return None


def get_es_data(doc_id):
    doc = fetch_es(doc_id)
    if doc and doc['_source']:
        try:
            sigs = list(json.loads(doc['_source']['signatures']).keys())
            return doc['_source']['title'], sigs
        except Exception as e:
            print(e)
    return None, None


def save_title(lookup_id, ltitle, match_id, mtitle):
    with open("titles", "a") as f:
        f.write("{} matches {}".format(lookup_id + " " + ltitle, match_id + " " + mtitle))
        f.write("\n")


def compare_doc(lookup_id, match_id):
    ltitle, lsig = get_es_data(lookup_id)
    mtitle, msig = get_es_data(match_id)
    shared_sigs = set(lsig) & set(msig)
    if len(shared_sigs) / len(lsig) < 0.8:
        print("falsy match with {} and {}".format(lookup_id, match_id))
        save_title(lookup_id, "falsy:"+ltitle, match_id, mtitle)
    else:
        save_title(lookup_id, "great:"+ltitle, match_id, mtitle)


def parse_match_block(match_block):
    global matches
    if not match_block: return
    lines = match_block.split('\n')
    lookup = lines[0]
    matches = lines[1:]

    for match in matches:
        if match:
            lookup_id = parse_id(lookup)
            match_id = parse_id(match)
            if found(matches, lookup_id, match_id):
                pass
            else:
                compare_doc(lookup_id, match_id)




if __name__ == '__main__':
    # LOOKUP_TAG = "INFO:root:looking"
    # MATCH_TAG = "INFO:root:matches"
    # with open("permute.log", "r") as f:
    #     match_block = None
    #     for line in f:
    #         if line and line.startswith(MATCH_TAG):
    #             match_block += line
    #         elif line and line.startswith(LOOKUP_TAG):
    #             parse_match_block(match_block)
    #             match_block = line
    #         else:
    #             parse_match_block(match_block)

    result = {}
    f = open("permute1.log", "r")
    for row in f.readlines():
        row = row.strip()
        if "matches" in row:
            words = row.split()
            id1 = eval(words[0][10:])
            id2 = eval(words[-1])
            try:
                if id2 in result[id1]:
                    pass
                else:
                    result[id1].append(id2)
            except:
                result[id1] = [id2]
    res = {}
    for i in sorted(result):
        res[i] = result[i]
    with open("..\\data\\result3.json", "w") as f:
        json.dump(res, f)
