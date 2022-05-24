import random
import statistics
from datetime import datetime

from evolution_statistics import EvolutionStatistic
from selection_methods import Selection


class Evolution:
    current_iter_num = 0

    def __init__(self, start_population, health_function, successful_round_condition, selection_class: Selection,
                 calc_noise, progin, genotype_phenotype_diagrams,
                 mutation_p=0, max_iter_num=10000000, accuracy=0.0001, should_draw_histogram=False, directory_name="RESULT"):
        self.selection_method = selection_class
        self.health_function = health_function
        self.max_iter_num = max_iter_num
        self.accuracy = accuracy
        self.start_population_with_health = [(i, self.health_function(i)) for i in start_population]
        self.population_with_health = [(i, self.health_function(i)) for i in start_population]
        self.statistics_class = EvolutionStatistic(self.population_with_health.copy(), successful_round_condition, calc_noise, max_iter_num)
        self.should_draw_histogram = should_draw_histogram
        self.n = len(self.population_with_health)
        self.mutation_p = mutation_p
        self.average_health = []
        self.progin = progin
        self.draw_genotype_phenotype_diagrams = genotype_phenotype_diagrams
        self.directory_name = directory_name

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
        for i in range(1, len(iter_health)):
            if abs(iter_health[i] - iter_health[i-1]) > self.accuracy:
                return False
        return True

    def should_stop_evolution(self):
        if self.mutation_p > 0:
            return self.current_iter_num >= self.max_iter_num or self.almost_equal()
        return self.current_iter_num >= self.max_iter_num or self.all_sequences_are_equal()

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

    def run_evolution(self):

        while not self.should_stop_evolution():
            if self.current_iter_num % 1000 == 0:
                print(f"{self.current_iter_num} {datetime.now().time()}")

            if self.current_iter_num < 5:
                self.draw_genotype_phenotype_diagrams(self.population_with_health, {"health_func": self.health_function,
                                                             "population_size": self.n, "mutation": self.mutation_p,
                                                             "iter": self.current_iter_num, "method": self.selection_method,
                                                            "progin": self.progin}, self.directory_name)
            # calculation
            parents_pool_with_health = self.selection_method.select_parents_pool(self.population_with_health)
            if self.mutation_p > 0:
                parents_pool = [i[0] for i in parents_pool_with_health]
                parents_pool_after_mutation = self.mutation(parents_pool, self.mutation_p)
                self.population_with_health = [(i, self.health_function(i)) for i in parents_pool_after_mutation]
            else:
                self.population_with_health = parents_pool_with_health
            self.current_iter_num += 1

            if len(self.average_health) > 9:
                self.average_health.pop(0)
            self.average_health.append(self.calc_average_health_in_population())

            self.statistics_class.update(self.population_with_health, self.current_iter_num)

        self.draw_genotype_phenotype_diagrams(self.population_with_health, {"health_func": self.health_function,
                                                     "population_size": self.n, "mutation": self.mutation_p,
                                                     "iter": self.current_iter_num, "method": self.selection_method,
                                                     "progin": self.progin, "final": True}, self.directory_name)
        stat = self.statistics_class.calc_stat()
        return self.population_with_health, stat