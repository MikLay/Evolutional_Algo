import random

from helpers import dec_to_grey


class PopulationGenerator:
    def __init__(self, sequences_len, perfect_item=None):
        self.sequences_len = sequences_len
        self.perfect_item = perfect_item or self.generate_optimal_sequence()

    def generate_population(self, population_size: int, add_perfect=False):
        """Generate population"""
        raise NotImplementedError

    def generate_optimal_sequence(self):
        return NotImplementedError


class FConstPopulationGenerator(PopulationGenerator):
    def generate_population(self, population_size: int, add_perfect=False):
        res = []
        for i in range(population_size // 2):
            res.append('0' * self.sequences_len)
            res.append('1' * self.sequences_len)
        # if the n is odd
        if len(res) < population_size:
            res.append('1' * self.sequences_len)
        return res


class BinomialPopulationGenerator(PopulationGenerator):
    def __init__(self, sequences_len, x1, x2, perfect_x):
        self.x1 = x1
        self.x2 = x2
        self.perfect_x = perfect_x
        perfect_item = dec_to_grey(self.perfect_x, self.x1, self.x2, l=sequences_len)
        super().__init__(sequences_len, perfect_item)

    def generate_optimal_sequence(self):
        return dec_to_grey(self.perfect_x, self.x1, self.x2, self.sequences_len)

    def generate_default_sequence(self, probability = 0.5):
        """Generate a sequence of random binary digits ('0' or '1') of the given length with a given probability of each digit."""
        return ''.join('1' if random.random() < probability else '0' for _ in range(self.sequences_len))

    def generate_population(self, population_size, add_perfect=True):
        res = []
        if add_perfect:
            res.append(self.perfect_item)
        while len(res) != population_size:
            # should I check if seq != optimal_sequence?
            res.append(self.generate_default_sequence())
        return res


class DecPopulationGenerator(PopulationGenerator):
    def __init__(self, sequences_len, get_x_by_y, x1, x2, y1, y2, perfect_x):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.perfect_x = perfect_x
        self.get_x_by_y = get_x_by_y
        perfect_item = dec_to_grey(self.perfect_x, self.x1, self.x2)
        super().__init__(sequences_len, perfect_item)

    def generate_population(self, population_size: int, add_perfect=False):
        mean = (self.y2 - self.y1) / 2
        scale = (self.y2 - self.y1) / 6
        res = []
        if add_perfect:
            res.append(dec_to_grey(self.perfect_x, self.x1, self.x2))
        while len(res) != population_size:
            r = round(random.gauss(mean, scale), 2)
            if self.y1 <= r <= self.y2:
                correspond_x = self.get_x_by_y(r)
                if len(correspond_x) == 2:
                    if random.random() < 0.5:
                        res.append(dec_to_grey(correspond_x[0], self.x1, self.x2))
                    else:
                        res.append(dec_to_grey(correspond_x[1], self.x1, self.x2))
                else:
                    res.append(dec_to_grey(correspond_x[0], self.x1, self.x2))
        return res
