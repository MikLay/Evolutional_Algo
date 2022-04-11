from draw_diagrams import draw_histogram
from evolution_statistics import EvolutionStatistic
from selection_methods import Selection


class Evolution:
    current_iter_num = 0

    def __init__(self, start_population, health_function, selection_class: Selection,
                 max_iter_num=10000000, draw_histogram=False):
        self.selection_method = selection_class
        self.health_function = health_function
        self.max_iter_num = max_iter_num
        self.start_population_with_health = [(i, self.health_function(i)) for i in start_population]
        self.population_with_health = [(i, self.health_function(i)) for i in start_population]
        self.statistics_class = EvolutionStatistic(self.population_with_health.copy())
        self.draw_histogram = draw_histogram
        self.n = len(self.population_with_health)

    def all_sequences_are_equal(self):
        base_sequence = self.population_with_health[0]
        for seq in self.population_with_health:
            if seq[0] != base_sequence[0]:
                return False
        return True

    def should_stop_evolution(self):
        return self.current_iter_num >= self.max_iter_num or self.all_sequences_are_equal()

    def run_evolution(self):

        while not self.should_stop_evolution():
            # diagram
            if self.draw_histogram:
                draw_histogram(self.population_with_health)

            # calculation
            self.population_with_health = self.selection_method.generate_new_population(self.population_with_health)
            self.current_iter_num += 1

            self.statistics_class.update(self.population_with_health, self.current_iter_num)

        if self.draw_histogram:
            draw_histogram(self.population_with_health)

        stat = self.statistics_class.calc_stat()
        return self.population_with_health, stat