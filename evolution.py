import statistics

from draw_diagrams import draw_histogram
from evolution_statistics import EvolutionStatistic
from mutation import mutation
from selection_methods import Selection


class Evolution:
    current_iter_num = 0

    def __init__(self, start_population, health_function, check_perfect_func, selection_class: Selection, calc_noise, progin,
                 mutation_p=0, max_iter_num=10000000, accuracy=0.0001, should_draw_histogram=False):
        self.selection_method = selection_class
        self.health_function = health_function
        self.max_iter_num = max_iter_num
        self.accuracy = accuracy
        self.start_population_with_health = [(i, self.health_function(i)) for i in start_population]
        self.population_with_health = [(i, self.health_function(i)) for i in start_population]
        self.statistics_class = EvolutionStatistic(self.population_with_health.copy(), check_perfect_func, calc_noise)
        self.should_draw_histogram = should_draw_histogram
        self.n = len(self.population_with_health)
        self.mutation_p = mutation_p
        self.average_health = []
        self.progin = progin

    def all_sequences_are_equal(self):
        base_sequence = self.population_with_health[0]
        for seq in self.population_with_health:
            if seq[0] != base_sequence[0]:
                return False
        return True

    def calc_average_health_in_population(self):
        return statistics.mean([i[1] for i in self.population_with_health])

    def almost_equal(self):
        if len(self.average_health) < 10:
            return False
        iter_health = self.average_health[-10:]
        min_health = min(iter_health)
        max_health = max(iter_health)
        # print(f"{self.current_iter_num}: {max_health - min_health}")
        # print(iter_health)
        return (max_health - min_health) <= self.accuracy

    def should_stop_evolution(self):
        if self.mutation_p > 0:
            return self.current_iter_num >= self.max_iter_num or self.almost_equal()
        return self.current_iter_num >= self.max_iter_num or self.all_sequences_are_equal()

    def run_evolution(self):

        while not self.should_stop_evolution():
            if self.current_iter_num < 5:
                draw_histogram(self.population_with_health, {"health_func": self.health_function,
                                                             "population_size": self.n, "mutation": self.mutation_p,
                                                             "iter": self.current_iter_num, "method": self.selection_method,
                                                            "progin": self.progin})
            # calculation
            parents_pool_with_health = self.selection_method.select_parents_pool(self.population_with_health)
            if self.mutation_p > 0:
                parents_pool = [i[0] for i in parents_pool_with_health]
                parents_pool_after_mutation = mutation(parents_pool, self.mutation_p)
                self.population_with_health = [(i, self.health_function(i)) for i in parents_pool_after_mutation]
            else:
                self.population_with_health = parents_pool_with_health
            self.current_iter_num += 1
            self.average_health.append(self.calc_average_health_in_population())

            self.statistics_class.update(self.population_with_health, self.current_iter_num)

        draw_histogram(self.population_with_health, {"health_func": self.health_function,
                                                     "population_size": self.n, "mutation": self.mutation_p,
                                                     "iter": self.current_iter_num, "method": self.selection_method,
                                                     "progin": self.progin, "final": True})
        stat = self.statistics_class.calc_stat()
        return self.population_with_health, stat