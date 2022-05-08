import random


class PopulationGenerator:
    def __init__(self, sequences_len, perfect_item=None):
        self.sequences_len = sequences_len
        self.perfect_item = perfect_item or self.generate_optimal_sequence()

    def generate_population(self, population_size: int):
        """Generate population"""
        raise NotImplementedError

    def generate_optimal_sequence(self):
        return NotImplementedError


class FConstPopulationGenerator(PopulationGenerator):
    def generate_population(self, population_size: int):
        res = []
        for i in range(population_size // 2):
            res.append('0' * self.sequences_len)
            res.append('1' * self.sequences_len)
        # if the n is odd
        if len(res) < population_size:
            res.append('1' * self.sequences_len)
        return res


class BinomialPopulationGenerator(PopulationGenerator):
    def generate_optimal_sequence(self):
        return '0' * self.sequences_len

    def generate_default_sequence(self):
        seq = ''
        for _ in range(self.sequences_len):
            if random.random() < 0.5:
                seq += '0'
            else:
                seq += '1'
        return seq

    def generate_population(self, population_size, add_perfect=True):
        res = []
        if add_perfect:
            res.append(self.perfect_item)
        while len(res) != population_size:
            # should I check if seq != optimal_sequence?
            res.append(self.generate_default_sequence())
        return res
