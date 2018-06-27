import itertools
import numpy as np
from elasticsearch import Elasticsearch
import logging


# TODO: how to make it faster?
def order_chunk_as_sequence(chunks, sequence):
    """
    :param chunks: [[0,1],[2,3],[4,5],[6,7]]
    :param sequence: [1,2]
    :return: [2,3,4,5,0,1,6,7]
    """
    result = []
    for i in sequence:
        result += chunks[i]
    for i, c in enumerate(chunks):
        if i in sequence:
            pass
        else:
            result += c
    return result


def bit_count(bit_chunks, cs):
    """
    :param bit_chunks: [[0,1],[2,3],[3,4]]
    :param cs:  [0,1]
    :return: len of part 0 + len of part 1, in this case, returns 4
    """
    result = 0
    for i in cs:
        result += len(bit_chunks[i])
    return result


def permutes(f, k=3, a=6):
    """
    The function generates multiple permute sequence, each function permute the f-bit integer to a new integer
    :param f: total f-bit integer
    :param k: let 3 parts
    :param a: total parts to divide
    :return: a list of permute functions
    """
    # split f bit into a parts, then combine to a-k's times
    bit_chunks = [i.tolist() for i in np.array_split(range(0, f), a)]
    chunk_sequence = list(itertools.combinations(range(0, a), a - k))
    bit_sequences = [order_chunk_as_sequence(bit_chunks, cs) for cs in chunk_sequence]
    count = [bit_count(bit_chunks, cs) for cs in chunk_sequence]
    # a sequence, and the first part counts
    return list(zip(bit_sequences, count))


def int_to_bits(a):
    return format(a if a >= 0 else (1<<64) + a, '064b')


def bits_to_int(b):
    return np.int64(np.uint64(int(b, 2))).item()


def rearrange_bits(aint, bit_sequence):
    bits = int_to_bits(aint)
    if len(bits) < 64:
        bits = '0' * (64 - len(bits)) + bits
    newbits = [bits[i] for i in bit_sequence]
    return bits_to_int(''.join(newbits))


def permute_int(aint):
    result = []
    for i,count in permutes(64):
        newint = rearrange_bits(aint, i)
        result.append((newint, count))
    return result


def range_int(aint, bit_count):
    bits = int_to_bits(aint)
    low = bits[0:bit_count] + '0' * (len(bits) - bit_count)
    high = bits[0:bit_count] + '1' * (len(bits) - bit_count)
    return (bits_to_int(low), bits_to_int(high))


def gen_perm(es, indoc='simhashes'):
    result = es.search(index=indoc, doc_type=indoc, body={"query": {"match_all": {}}}, scroll='1m')
    while result and result['hits']['hits']:
        for r in result['hits']['hits']:
            xid = r['_id']
            file = r['_source']['file']
            logging.info("gen permutations for {}".format(xid))
            hashval = r['_source']['hashval']
            ints = [i for i,j in permute_int(hashval)]
            names = ["perm" + str(i) for i in range(0, len(ints))]
            name_int = {n:i for (n,i) in zip(names, ints)}
            name_int['file'] = file
            try:
                es.update(index=indoc, doc_type=indoc, id=xid, body={"doc":name_int})
            except Exception as e:
                logging.error(e)
        result = es.scroll(result['_scroll_id'], scroll='1m')
        #result = None


def distance(a, b):
    return bin(a ^ b).count('1')


def query_distance_3(es, oid, key, val, low, high, indoc='simhash'):
    result = es.search(index=indoc,
                       doc_type=indoc,
                       body={"query": {"range":
                                           {key: {"gte": low,
                                                  "lte": high,
                                                  "boost": 2.0}}}},
                       scroll='1m')
    while result and result['hits']['hits']:
        for doc in result['hits']['hits']:
            xid = doc['_id']
            hashval = doc['_source'].get(key)
            if distance(hashval, val) <= 3 and oid != xid:
                logging.info("{} matches {}".format(oid, xid))
        result = es.scroll(result['_scroll_id'], scroll='1m')


def query_perm(es, indoc='simhashes'):
    try:
        result = es.search(index=indoc, doc_type=indoc, body={"query": {"match_all": {}}}, scroll='1m')
        counts = [j for i,j in permutes(64)]
        while result and result['hits']['hits']:
            for doc in result['hits']['hits']:
                xid = doc['_id']
                logging.info("looking at {}".format(xid))
                for i in range(20):
                    k = "perm" + str(i)
                    v = doc['_source'].get(k)
                    int_range = range_int(v, counts[i])
                    try:
                        query_distance_3(es, xid, k, v, int_range[0], int_range[1], indoc)
                    except Exception as e:
                        logging.error(e)
            while True:
                try:
                    result = es.scroll(result['_scroll_id'], scroll="1m")
                    break
                except Exception as e:
                    logging.error(e)
    except Exception:
        logging.critical("es search failed")
        exit(1)


if __name__ == '__main__':
    """
    For testing purpose
    """
    # print(order_chunk_as_sequence([[0,1],[2,3],[4,5]], [0,2]))
    # print(list(permutes(64, 3, 6)))
    #print(len(permute_int(7135637346109630000)))
    # x = range_int(7135637346109630000, 31)
    #print(x[0])
    # print(x[1])
    logging.basicConfig(filename="permute.log", level=logging.INFO)
    es = Elasticsearch([{'host':'icam-prod-ms-20','port':9200}])
    gen_perm(es)
    # logging.getLogger('elasticsearch').setLevel(logging.CRITICAL)  # or desired level
    # query_perm(es, 'simhashes')

    # print(permute_int(15517852168334194449))
    # print(int_to_bits(15517852168334194449))
    # print(bin(15517852168334194449)[2:])
    # print(bits_to_int("1101011101011010011111000101010001111010100101011011011100010001"))
    # print(int("1101011101011010011111000101010001111010100101011011011100010001",2))
    # print(np.uint64(int("1101011101011010011111000101010001111010100101011011011100010001",2)))
    # print(np.int64(np.uint64(int("1101011101011010011111000101010001111010100101011011011100010001",2))))
    # ints = [i for i,j in permute_int(15517852168334194449)]
    # names = ["perm" + str(i) for i in range(0, len(ints))]
    # name_int = {n:str(i) for (n,i) in zip(names, ints)}

    # print(name_int)