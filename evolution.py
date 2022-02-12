import statistics


class Evolution:
    current_iter_num = 0

    def __init__(self, start_population, health_function, selection_method, additional_params, max_iter_num=10000000):
        self.selection_method = selection_method
        self.health_function = health_function
        self.max_iter_num = max_iter_num
        self.population = start_population
        self.additional_params = additional_params

    def all_sequences_are_equal(self):
        base_sequence = self.population[0]
        for seq in self.population:
            if seq != base_sequence:
                return False
        return True

    def should_stop_evolution(self):
        return self.current_iter_num >= self.max_iter_num or self.all_sequences_are_equal()

    def run_evolution(self):
        while not self.should_stop_evolution():
            print(f"iter {self.current_iter_num}")
            print(statistics.mean([self.health_function(i) for i in self.population]))
            self.population = self.selection_method(self.population, self.health_function, **self.additional_params)
            self.current_iter_num += 1

        return self.population