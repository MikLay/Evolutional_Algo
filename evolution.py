import random
import statistics
import queue
from datetime import datetime

from evolution_statistics import EvolutionStatistic
from selection_methods import Selection


class Evolution:
    current_iter_num = 0

    def __init__(self, start_population, health_function, successful_round_condition, selection_class: Selection,
                 calc_noise, progin, genotype_phenotype_diagrams,
                 mutation=False, mutation_p=0, crossover=False,directory_name="RESULT",should_draw_histogram=False, max_iter_num=10000000, accuracy=0.0001, max_generations=10):
        self.selection_method = selection_class
        self.health_function = health_function
        self.max_iter_num = max_iter_num
        self.accuracy = accuracy
        self.population_with_health = [(i, self.health_function(i)) for i in start_population]
        self.statistics_class = EvolutionStatistic(self.population_with_health.copy(), successful_round_condition, calc_noise, max_iter_num)
        self.should_draw_histogram = should_draw_histogram
        self.sequence_len = len(start_population[0])
        self.n = len(self.population_with_health)
        self.crossover = crossover
        self.max_generations = max_generations
        # mutation due to table of mutations
        self.mutation = mutation
        self.mutation_p = mutation_p
        self.average_health = []
        self.progin = progin
        self.draw_genotype_phenotype_diagrams = genotype_phenotype_diagrams
        self.directory_name = directory_name

    def all_sequences_are_equal(self):
        base_sequence = self.population_with_health[0][0]
        return all(sequence[0] == base_sequence for sequence in self.population_with_health)

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
        if self.mutation or self.crossover:
            return (self.current_iter_num >= self.max_iter_num) or self.almost_equal()
        return (self.current_iter_num >= self.max_iter_num) or self.all_sequences_are_equal()

    @staticmethod
    def mutate(population, mutation_rate):
        """Perform a bit mutation with mutation_rate on the population list."""
        mutated_sequences = []
        for sequence in population:
            mutated_sequence = ''
            for bit in sequence:
                if random.random() < mutation_rate:
                    mutated_bit = '0' if bit == '1' else '1'
                else:
                    mutated_bit = bit
                mutated_sequence += mutated_bit
            mutated_sequences.append(mutated_sequence)
        return mutated_sequences

    @staticmethod
    def make_crossover(population):
        """Perform a single-point crossover on the population list."""
        if len(population) < 2:
            return self.sequences

        # Choose a random index to perform the crossover
        crossover_index = random.randint(0, len(population[0]) - 1)

        # Perform the crossover on each pair of adjacent sequences in the list
        for i in range(0, len(population) - 1, 2):
            seq1 = population[i]
            seq2 = population[i+1]
            population[i] = seq1[:crossover_index] + seq2[crossover_index:]
            population[i+1] = seq2[:crossover_index] + seq1[crossover_index:]

        return population

    def run_evolution(self):

        while not self.should_stop_evolution():
            if self.current_iter_num % 1000 == 0:
                print(f"{self.current_iter_num} {datetime.now().time()}")

            if self.current_iter_num < 5:
                self.draw_genotype_phenotype_diagrams(self.population_with_health, {"health_func": self.health_function,
                                                             "population_size": self.n, "mutation": self.mutation, "mutation_p": self.mutation_p,
                                                             "iter": self.current_iter_num, "method": self.selection_method,
                                                            "progin": self.progin, "crossover": self.crossover}, self.directory_name)
            # shuffle
            random.shuffle(self.population_with_health)
            # selection
            parents_pool_with_health = self.selection_method.select_parents_pool(self.population_with_health)

            # selected items after mutation
            selected_items = self.statistics_class.selected_items(self.population_with_health, parents_pool_with_health)

            # mutations
            if self.mutation or self.crossover:
                parents_pool_after_mutation = [i[0] for i in parents_pool_with_health]
                # if crossover
                if self.crossover:
                    parents_pool_after_mutation = self.make_crossover(parents_pool_after_mutation)
                # if mutation
                if self.mutation:
                    parents_pool_after_mutation = self.mutate(parents_pool_after_mutation, self.mutation_p)
                self.population_with_health = [(i, self.health_function(i)) for i in parents_pool_after_mutation]
            else:
                self.population_with_health = parents_pool_with_health
            self.current_iter_num += 1

            # Hold only 10 generations average_health
            if len(self.average_health) > self.max_generations-1:
                self.average_health.pop(0)
            self.average_health.append(self.calc_average_health_in_population())

            # Iteration update
            self.statistics_class.update(self.population_with_health, self.current_iter_num, selected_items)


        self.draw_genotype_phenotype_diagrams(self.population_with_health, {"health_func": self.health_function,
                                                     "population_size": self.n, "mutation": self.mutation, "mutation_p": self.mutation_p,
                                                     "iter": self.current_iter_num, "method": self.selection_method,
                                                     "progin": self.progin, "final": True, "crossover": self.crossover}, self.directory_name)
        stat = self.statistics_class.calc_stat()
        return self.population_with_health, stat