"""
To generate ngram from input data, and save to python local db
"""
import sys
from nlp import tokenize, remove_stopword, stem_word, punc_filter, one_gram, bi_gram, tri_gram
from elasticsearch import Elasticsearch, helpers


END_SIGN = "---END.OF.DOCUMENT---"


def ngram(text, least_appear=3):
    tokens = stem_word(remove_stopword(tokenize(text)));
    ngram1 = [k for k,v in one_gram(tokens).items() if v >= least_appear]
    ngram2 = [k for k,v in bi_gram(tokens).items() if v >= least_appear]
    ngram3 = [k for k,v in tri_gram(tokens).items() if v >= least_appear]
    return ngram1 + \
           [' '.join(i) for i in ngram2] + \
           [' '.join(i) for i in ngram3]


def bulk_create(index, doc_type, nonexists):
    return [{"_op_type": "create",
             "_index": index,
             "_type": doc_type,
             "_id": i,
             "article_count":1} for i in nonexists]


def bulk_update(index, doc_type, exists):
    return [{"_op_type": "update",
             "_index": index,
             "_type": doc_type,
             "_id": i,
             "script": {"source": "ctx._source.article_count += 1",
                        "lang": "painless"}} for i in exists]


def save(ngrams, es):
    if not ngrams: return
    index = 'ngram'
    doc_type = 'ngram'

    exists, nonexists = [], []
    results = (es.mget(index=index, doc_type=doc_type, body={"ids": ngrams}))['docs']

    for result in results:
        if result['found']:
            exists.append(result['_id'])
        else:
            nonexists.append(result['_id'])

    bulks = bulk_create(index, doc_type, nonexists) + bulk_update(index, doc_type, exists)
    helpers.bulk(es, bulks)

def analyze(f, es):
    total = 0
    with open(f, "r") as f:
        article = ""
        for line in f:
            if line.strip() == END_SIGN:
                print(total)
                if total >= 100000:
                    exit(0)
                save(ngram(article), es)
                article = ""
                total += 1
            else:
                article += line


if __name__ == '__main__':
    es = Elasticsearch()
    es.search()
    analyze(sys.argv[1], es)
