import csv
import statistics

import numpy


class EvolutionStatistic:
    def __init__(self, start_population_with_health):
        self._start_population = start_population_with_health
        self._n = len(start_population_with_health)

        self._current_population = start_population_with_health
        self._current_iter = 0
        # self._selection_intensity_arr = []
        self._repr_speed = []
        self._selection_diffs = []
        self._health_and_percent_of_the_best_arr = [self.num_of_the_best(start_population_with_health)]
        self._avarage_health_arr = [self.avg_health_in_population(start_population_with_health)]
        self._sigma_arr = [self.calc_sigma(start_population_with_health)]

    def update(self, population_with_health, current_iter_num):
        selected_items = self.selected_items(self._current_population, population_with_health)
        self._repr_speed.append((self.calc_rr(self._current_population, selected_items), self._current_iter))
        self._selection_diffs.append((self.calc_selection_diff(self._current_population, selected_items), self._current_iter))
        self._current_population = population_with_health.copy()
        self._current_iter = current_iter_num
        self._curr_avg_health = self.avg_health_in_population(population_with_health)
        self._health_and_percent_of_the_best_arr.append(self.num_of_the_best(population_with_health))
        self._avarage_health_arr.append(self.avg_health_in_population(population_with_health))
        self._sigma_arr.append(self.calc_sigma(population_with_health))
        # self._selection_intensity_arr.append((self.calc_selection_intensity(), self._current_iter))
        # growth rate

    def selected_items(self, old_population_with_health, new_population_with_health):
        res = []
        new_p = [i[0] for i in new_population_with_health]
        for old_item in old_population_with_health:
            if old_item[0] in new_p:
                res.append(old_item)
        return res

    def calc_rr(self, old_population_with_health, selected_items_with_health):
        return len(selected_items_with_health) / len(old_population_with_health)

    def calc_selection_diff(self, old_population_with_health, selected_items):
        return self.avg_health_in_population(selected_items) - self.avg_health_in_population(old_population_with_health)

    def num_of_the_best(self, population_with_health):
        the_best = sorted(population_with_health, key=lambda i: i[1])[-1]
        count = 0
        for i in population_with_health:
            # no need to check sequence if health is different
            if i[1] == the_best[1] and i[0] == the_best[0]:
                count += 1
        return the_best[1], count / self._n

    @staticmethod
    def the_best_health_in_population(population_with_health):
        return max([i[1] for i in population_with_health])

    @staticmethod
    def avg_health_in_population(population_with_health):
        return statistics.mean([i[1] for i in population_with_health])

    @staticmethod
    def calc_sigma(population_with_health):
        return numpy.std([i[1] for i in population_with_health])

    def calc_selection_intensity(self):
        a_c = self._curr_avg_health
        a_s = self._start_avg_health
        s = self._sigma
        return (a_c - a_s) / s

    def calc_NI(self):
        # todo set - if didn't reach homogeneity
        return self._current_iter

    def calc_selection_intensity_arr(self):
        def calc_selection_intensity(fs, f, sigma):
            return (fs - f) / sigma

        selection_intensity_arr = []
        for i in range(1, len(self._avarage_health_arr)):
            intensity = calc_selection_intensity(self._avarage_health_arr[i], self._avarage_health_arr[i-1], self._sigma_arr[i-1])
            selection_intensity_arr.append((intensity, i))
        return selection_intensity_arr

    def calc_growth_rate_arr(self):
        def calc_growth_rate(i):
            if self._health_and_percent_of_the_best_arr[i][0] == self._health_and_percent_of_the_best_arr[i - 1][0]:
                return self._health_and_percent_of_the_best_arr[i][1] / self._health_and_percent_of_the_best_arr[i - 1][
                    1]
            else:
                return 0

        growth_rate = []
        for i in range(1, len(self._health_and_percent_of_the_best_arr)):
            growth_rate.append((calc_growth_rate(i), i, self._health_and_percent_of_the_best_arr[i][1]))
        return growth_rate

    def calc_stat(self):
        """
        calc parameters based on population data
        """
        current_population_statistics = {}

        # base data
        current_population_statistics["NI"] = self.calc_NI()
        current_population_statistics["F_found"] = self.the_best_health_in_population(self._current_population)
        current_population_statistics["F_avg"] = self.avg_health_in_population(self._current_population)

        # calc intensity
        selection_intensity = self.calc_selection_intensity_arr()
        min_selection_intensity = sorted(selection_intensity, key=lambda i: i[0])[0]
        max_selection_intensity = sorted(selection_intensity, key=lambda i: i[0], reverse=True)[0]
        current_population_statistics["I_min"] = min_selection_intensity[0]
        current_population_statistics["NI_I_min"] = min_selection_intensity[1]
        current_population_statistics["I_max"] = max_selection_intensity[0]
        current_population_statistics["NI_I_max"] = max_selection_intensity[1]
        current_population_statistics["I_avg"] = statistics.mean([i[0] for i in selection_intensity])

        # growth rate
        growth_rate = self.calc_growth_rate_arr()
        current_population_statistics["GR_early"] = growth_rate[1][0]
        current_population_statistics["GR_avg"] = statistics.mean([i[0] for i in growth_rate])
        more_than_50_percent = list(filter(lambda x: x[2] >= 0.5, growth_rate))
        current_population_statistics["GR_late"] = more_than_50_percent[0][0]
        current_population_statistics["NI_GR_late"] = more_than_50_percent[1][1]

        # diversity
        min_rr = sorted(self._repr_speed, key=lambda i: i[0])[0]
        max_rr = sorted(self._repr_speed, key=lambda i: i[0], reverse=True)[0]
        current_population_statistics["RR_min"] = min_rr[0]
        # todo can be on several iterations
        current_population_statistics["NI_RR_min"] = min_rr[1]
        current_population_statistics["RR_max"] = max_rr[0]
        current_population_statistics["NI_RR_max"] = max_rr[1]
        current_population_statistics["RR_avg"] = statistics.mean([i[0] for i in self._repr_speed])

        current_population_statistics["Teta_min"] = 1 - max_rr[0]
        current_population_statistics["NI_Teta_min"] = max_rr[1]
        current_population_statistics["NI_Teta_max "] = 1 - min_rr[0]
        current_population_statistics["NI_RR_max "] = min_rr[1]
        current_population_statistics["Teta_avg"] = statistics.mean([(1 - i[0]) for i in self._repr_speed])

        # selection difference
        min_diff = sorted(self._selection_diffs, key=lambda i: i[0])[0]
        max_diff = sorted(self._selection_diffs, key=lambda i: i[0], reverse=True)[0]
        current_population_statistics["s_min"] = min_diff[0]
        current_population_statistics["NI_s_min"] = min_diff[1]
        current_population_statistics["s_max"] = max_diff[0]
        current_population_statistics["NI_s_max"] = max_diff[1]
        current_population_statistics["s_avg"] = statistics.mean([i[0] for i in self._selection_diffs])

        return current_population_statistics



