# coding: utf-8
import math
import sys
from elasticsearch import Elasticsearch
import hashlib
import uuid
import json
import numpy as np
import logging
from nlp import tokenize, stem_word, remove_stopword, one_gram, bi_gram, tri_gram


"""
A simhash trial to: 
    1 extract feature,
    2 measure weight with TF/IDF,
    3 calculate simhash with weighted feature 
"""


END_SIGN = "---END.OF.DOCUMENT---"


def idf(words, n=100000, es=None):
    """
    Args:
        fq: frequency distribution instance
        n: total document number
        words: a list of words&phrases from the target document
    Returns:
        a dict includes {word&phrase: idf weight}
    """
    if es is None:
        logging.error("ES connection lost. Exiting.")
        sys.exit(1)
    try:
        results = es.mget(index='ngram', doc_type='ngram', body={"ids":list(words)})
        if results and results['docs']:
            words_weight = {}
            for r in results['docs']:
                word = r['_id']
                count = 1 + r['_source']['article_count'] if r['found'] else 1
                words_weight[word] = math.log2(n / count)
            logging.info(words_weight)
            return words_weight
        return {w: 1 for w in words}
    except Exception as e:
        logging.error(words)
        logging.error(e.info)
        return {w: 1 for w in words}


# TODO: a better hash function
# this one returns 128 bit int, more than 64.
def _hash(x):
    return int(hashlib.md5(x.encode("utf-8")).hexdigest(), 16)


def calculate_simhash(weighted_features, f=64):
    v = [0] * f
    masks = [1 << i for i in range(f)]
    for feature, weight in weighted_features.items():
        h = _hash(feature)
        for i in range(f):
            v[i] = v[i] + weight if h & masks[i] else v[i] - weight
    value = 0
    for i in range(f):
        if v[i] > 0:
            value |= masks[i]
    return value


def distance(a, b):
    return bin(a ^ b).count('1')


def headline(src):
    # return the first non-empty line as title.
    lines = src.split("\n")
    for l in lines:
        if l.strip() != "":
            return l


def extract_feature(words, least_appear=3):
    tokens = stem_word(remove_stopword(words))
    ngram1 = [k for k,v in one_gram(tokens).items() if v >= least_appear]
    ngram2 = [' '.join(k) for k,v in bi_gram(tokens).items() if v >= least_appear]
    ngram3 = [' '.join(k) for k,v in tri_gram(tokens).items() if v >= least_appear]
    return ngram1 + ngram2 + ngram3


def extract_feature_with_tf(words, least_appear=3):
    tokens = stem_word(remove_stopword(words))
    one_fd, bi_fd, tri_fd = one_gram(tokens), bi_gram(tokens), tri_gram(tokens)
    one_tf = {k:one_fd.freq(k) for k,v in one_fd.items() if v >= least_appear}
    bi_tf = {' '.join(k):bi_fd.freq(k) for k,v in bi_fd.items() if v >= least_appear }
    tri_tf = {' '.join(k):tri_fd.freq(k) for k,v in tri_fd.items() if v >= least_appear}
    return {**one_tf, **bi_tf, **tri_tf}


# use idf only
def pick_features_idf(idf_f, n=15):
    top_features = sorted(idf_f, key=idf_f.get, reverse=True)[:n]
    return {k:idf_f[k] for k in top_features}


def covered(f, top_n_f):
    for chosen in top_n_f:
        if f == chosen:
            logging.info("this should not happen")
            return True
        elif f in chosen:
            return True
        else:
            pass
    return False


# consider one-gram may be included in bi-gram
# one-gram, bi-gram may be included in tri-gram
def pick_features_xf_exclusive(idf_f, n=15):
    sorted_idf_f = sorted(idf_f, key=idf_f.get, reverse=True)
    logging.info(sorted_idf_f)
    top_n = []
    for f in sorted_idf_f:
        if covered(f, top_n):
            continue
        same_idf_fs = [k for k,v in idf_f.items() if v == idf_f[f] and k != f]
        if covered(f, same_idf_fs):
            continue
        top_n.append(f)
        if len(top_n) == n:
            break
    return {k:idf_f[k] for k in top_n}


def pick_features_1_23(idf_f, tf_f, n=15):
    """
    pick 5 one-gram, using tf as threshold and idf as ranking
    pick 5 bi-gram and 5 tri-gram, use tf as ranking
    """
    count23 = int(n / 3 * 2)
    count1 = n - count23
    top23, top1 = [], []
    tf_f23 = {k:v for k,v in tf_f.items() if len(k.split(" ")) >1}
    picked23 = pick_features_xf_exclusive(tf_f23, count23)
    top23 = picked23.keys()
    sorted_idf_f = sorted(idf_f, key=idf_f.get, reverse=True)
    for f in sorted_idf_f:
        if len(f.split(" ")) == 1 and not covered(f, top23):
            top1.append(f)
            if len(top1) == count1:
                break
    return {k:idf_f[k] for k in list(top23) + top1}


def format_src(src):
    return stem_word(remove_stopword(tokenize(src)))


def simhash(src, es):
    words = format_src(src)
    count = len(words)
    if count < 500:
        return "", 0, {}

    # features = extract_feature(words)
    tf_features = extract_feature_with_tf(words)
    idf_features = idf(tf_features.keys(), 3035115, es)
    # weighted_features = {k:v*tf_features[k] for k,v in idf_features.items()}
    top_features = pick_features_1_23(idf_features, tf_features)
    logging.info("top features are : {}".format(top_features))
    return headline(src), calculate_simhash(top_features), top_features


def save(title, hash_val, signatures, es):
    try:
        es.create(id=uuid.uuid1(), index="simhash", doc_type="simhash",
                  body={"title": title, "hashval": hash_val, "signatures": json.dumps(signatures)})
    except Exception as e:
        logging.error(signatures)
        logging.error(e.info)


def main(src):
    es = Elasticsearch()
    with open(src) as f:
        article = ""
        for line in f:
            if line.strip() == END_SIGN:
                title, hash_val, signatures = simhash(article, es)
                if len(signatures) > 0:
                    save(title, np.int64(np.uint64(hash_val)).item(), signatures, es)
                    article = ""
            else:
                article += line
        # handling EOF as end of file


if __name__ == '__main__':
    logging.basicConfig(filename="simhash.log", level=logging.INFO)
    main(sys.argv[1])
