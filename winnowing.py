import hashlib

def kgrams(text, k=7):
    text = list(text)
    n = len(text)
    texts = []
    if n < k:
        yield text
    else:
        for i in range(n - k + 1):
            yield text[i:i+k]


def winnowing_hash(kgram):
    kgram = zip(*kgram)
    kgram = list(kgram)
    if len(kgram) > 1:
        text = ''.join(kgram[1])
    else:
        text = ''
    hs = hashing(text)
    return (kgram[0][0] if len(kgram) > 1 else -1, hs)


def hashing(text):
    hs = hashlib.sha1(text.encode('utf-8'))
    hs = hs.hexdigest()[-4:]
    hs = int(hs, 16)
    return hs


def select_min(window):
    return min(window, key = lambda x: x[1])


def winnow(text, k=7):
    n = len(list(text))
    text = zip(range(n), text)
    hashes = map(lambda x: winnowing_hash(x), kgrams(text, k))
    windows = kgrams(hashes, 5)
    return set(map(select_min, windows))
