# python file to compute resemblence

def resemblence(test1, test2, k):

    list1 = sorted(list(test1))
    list2 = sorted(list(test2))

    if len(list1) > k:
        list1 = list1[:k]
    if len(list2) > k:
        list2 = list2[:k]

    w1 = set(list1)
    w2 = set(list2)

    list12 = sorted(list(w1.union(w2)))
    if len(list12) > k:
        list12 = list12[:k]
    w12 = set(list12)

    resemble_rate = len((w1.intersection(w2)).intersection(w12)) / len(w12)

    return resemble_rate