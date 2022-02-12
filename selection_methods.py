import random


def choose_candidates(population, t):
    indexes = []
    while len(indexes) != t:
        new_index = max(round(random.random() * len(population)-1), 0)
        if new_index not in indexes:
            indexes.append(new_index)
    return [population[i] for i in indexes]


def tournament_with_return(population, health_fun, p):
    # todo make a param
    t = 2
    n = len(population)
    new_population = []
    while len(new_population) != n:
        candidates = choose_candidates(population, t)
        candidates_with_health = [(candidate, health_fun(candidate)) for candidate in candidates]
        if random.random() <= p:
            rate = sorted(candidates_with_health, key=lambda tup: tup[1], reverse=True)
        else:
            rate = sorted(candidates_with_health, key=lambda tup: tup[1])
        new_population.append(rate[0][0])
    return new_population


def tournament_without_return(population, health_fun, p):
    # todo make a param
    t = 2
    second_copy = population.copy()
    current_population = population
    n = len(population)
    new_population = []
    while len(new_population) != n:
        # todo fix for odd number
        if len(current_population) < t:
            current_population = second_copy
        candidates = choose_candidates(current_population, t)
        for c in candidates:
            current_population.remove(c)
        candidates_with_health = [(candidate, health_fun(candidate)) for candidate in candidates]
        if random.random() <= p:
            rate = sorted(candidates_with_health, key=lambda tup: tup[1], reverse=True)
        else:
            rate = sorted(candidates_with_health, key=lambda tup: tup[1])
        new_population.append(rate[0][0])

    return new_population
