import random


def mutation(population, p):
    res = []
    for item in population:
        list_item = list(item)
        for i in range(len(list_item)):
            if random.random() < p:
                if list_item[i] == '0':
                    list_item[i] = '1'
                else:
                    list_item[i] = '0'
        res.append(''.join(list_item))
    return res
