import random


def init_f_const(n, l):
    res = []
    for i in range(n // 2):
        res.append('0' * l)
        res.append('1' * l)
    # if the n is odd
    if len(res) < n:
        res.append('1' * l)


def init_normal(n, l, optimal_sequence):
    res = [optimal_sequence]
    for i in range((n-1)):
        seq = ""
        for j in range(l):
            if random.random() < 0.5:
                seq += '0'
            else:
                seq += '1'
        # should I check if seq != optimal_sequence?
        res.append(seq)
    return res

