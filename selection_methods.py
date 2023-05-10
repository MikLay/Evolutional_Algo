import random


def choose_candidates(population, t):
    return random.sample(population, t)


class Selection:
    def select_parents_pool(self, population_with_health):
        raise NotImplementedError


class TournamentWithReturnSelection(Selection):
    def __init__(self, p):
        self.name = f"tournament_with_return_p_{p}"
        self.p = p

    def select_parents_pool(self, population_with_health):
        """
        population_with_health [(candidate, health_fun(candidate))]
        t (number of candidates) == 2
        """
        n = len(population_with_health)
        new_population = [max(choose_candidates(population_with_health, 2), key=lambda tup: tup[1])
                          if random.random() <= self.p
                          else min(choose_candidates(population_with_health, 2), key=lambda tup: tup[1])
                          for _ in range(n)]
        return new_population


class TournamentWithoutReturnSelection(Selection):
    def __init__(self, p):
        self.name = f"tournament_without_return_p_{p}"
        self.p = p

    def select_parents_pool(self, population_with_health):
        """
        population_with_health [(candidate, health_fun(candidate))]
        t (number of candidates) == 2
        """
        # as t == 2, make 2 copy of population
        current_population = population_with_health.copy()
        new_population = []
        while len(new_population) != len(population_with_health) and len(current_population) != 0:
            if len(current_population) == 1:
                new_population.append(current_population.pop())
                continue
            candidates = choose_candidates(current_population, 2)
            if random.random() <= self.p:
                rate = sorted(candidates, key=lambda tup: tup[1], reverse=True)
            else:
                rate = sorted(candidates, key=lambda tup: tup[1])

            current_population.remove(rate[1])
            new_population.append(rate[0])

        return new_population


class LinearRankingSelection(Selection):
    def __init__(self, b):
        self.name = f"linear_ranking_selection_b_{b}"
        self.b = b

    def p_linear_rank(self, value, N):
        return (2-self.b)/N + (2 * value * (self.b-1))/(N*(N-1))

    def calc_p(self, population):
        N = len(population)
        sorted_population = sorted(population, key=lambda tup: tup[1], reverse=True)
        res = []
        prev_val = 0
        for i in range(N):
            rang = N - i - 1
            p = self.p_linear_rank(rang, N)
            new_val = prev_val + p
            res.append((sorted_population[i][0], sorted_population[i][1], (prev_val, new_val)))
            prev_val = new_val
        return res

    def select_parents_pool(self, population_with_health):
        population_with_p_values = self.calc_p(population_with_health)
        n = len(population_with_health)
        step = 1 / n

        def get_item_by_sus_position(sus_position):
            # todo optimize
            for i in range(n):
                if population_with_p_values[i][2][0] <= sus_position < population_with_p_values[i][2][1]:
                    return (population_with_p_values[i][0], population_with_p_values[i][1])

        current_position = random.random()
        new_population = []
        while len(new_population) != n:
            new_population.append(get_item_by_sus_position(current_position))
            new_pos = current_position + step
            current_position = new_pos if new_pos < 1 else new_pos - 1
        return new_population