def res_con(test1, test2, k):

    # 300 is just a test number, can change
    list1 = sorted(list(test1))[:k]
    list2 = sorted(list(test2))[:k]
    
    w1 = set(list1)
    w2 = set(list2)
    w12 = set(sorted(list(w1.union(w2))[:k]))

    resemble = len(w1.intersection(w2).intersection(w12)) / len(w12)

    return resemble