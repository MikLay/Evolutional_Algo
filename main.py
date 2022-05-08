# from draw_diagrams import draw_health_distribution
import csv
import statistics

from draw_diagrams import draw_histogram
from evolution import Evolution
from health_functions import fh, fhd_10, fhd_50, fhd_150, fconst, grey_x_2, grey_x, grey_x_4, grey_2_x_2, grey_512_x_2, \
    grey_512_x_4, grey_e_x_025, grey_e_x_1, grey_e_x_2
from helpers import dec_to_grey
from init_sequences import BinomialPopulationGenerator, FConstPopulationGenerator

# Варіант 10
# Турнірний стохастичний без повернення, t=2; p=0.6, p=0.8
# Турнірний стохастичний з поверненням, t=2; p=0.6, p=0.8
# За рангом лінійний, β=1.6, β=1.2
from perfect_sequence import fh_perfect_sequence, f_const_perfect_sequence, perfect_sequence_1023, perfect_sequence_0
from report_creator import ReportCreator
from selection_methods import TournamentWithReturnSelection, TournamentWithoutReturnSelection, LinearRankingSelection


def print_sequence_data(sequences_with_health, title):
    if sequences_with_health:
        # print sequence and draw diagram
        # print(sequences_with_health)
        seq_freq = {}
        for i in sequences_with_health:
            if i[0] in seq_freq:
                seq_freq[i[0]] += 1
            else:
                seq_freq[i[0]] = 1
        for i in seq_freq.items():
            print(i)
        draw_histogram(sequences_with_health, title)
        sequences_health = [i[1] for i in sequences_with_health]
        print(f"sequence len: {len(sequences_with_health[0][0])}")
        print(f"population num: {len(sequences_health)}")
        print(f"max health: {max(sequences_health)}")
        print(f"min health: {min(sequences_health)}")
        print(f"statistics.mean health: {statistics.mean(sequences_health)}")


def main():
    # clean file
    file_name = "report_12.csv"
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([""])

        # population sizes
        population_sizes = [100, 500, 1000]

        # health functions
        params = [
            {"population_generator": FConstPopulationGenerator(sequences_len=100), "health_func": fconst,
             "perfect_item_func": f_const_perfect_sequence, "calc_noise": True},
            {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fh,
             "perfect_item_func": fh_perfect_sequence},
            {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fhd_10,
             "perfect_item_func": fh_perfect_sequence},
            {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fhd_50,
             "perfect_item_func": fh_perfect_sequence},
            {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fhd_150,
             "perfect_item_func": fh_perfect_sequence},
            {"population_generator": BinomialPopulationGenerator(sequences_len=10,
                                                                 perfect_item=dec_to_grey(10.23, 0, 10.23)),
             "health_func": grey_x_2, "perfect_item_func": perfect_sequence_1023},
            {"population_generator": BinomialPopulationGenerator(sequences_len=10,
                                                                 perfect_item=dec_to_grey(10.23, 0, 10.23)),
             "health_func": grey_x, "perfect_item_func": perfect_sequence_1023},
            {"population_generator": BinomialPopulationGenerator(sequences_len=10,
                                                                 perfect_item=dec_to_grey(10.23, 0, 10.23)),
             "health_func": grey_x_4, "perfect_item_func": perfect_sequence_1023},
            {"population_generator": BinomialPopulationGenerator(sequences_len=10,
                                                                 perfect_item=dec_to_grey(0, -5.11, 5.12)),
             "health_func": grey_512_x_2, "perfect_item_func": perfect_sequence_0},
            {"population_generator": BinomialPopulationGenerator(sequences_len=10,
                                                                 perfect_item=dec_to_grey(0, -5.11, 5.12)),
             "health_func": grey_512_x_4, "perfect_item_func": perfect_sequence_0},
            {"population_generator": BinomialPopulationGenerator(sequences_len=10,
                                                                 perfect_item=dec_to_grey(10.23, 0, 10.23)),
             "health_func": grey_e_x_025, "perfect_item_func": perfect_sequence_1023},
            {"population_generator": BinomialPopulationGenerator(sequences_len=10,
                                                                 perfect_item=dec_to_grey(10.23, 0, 10.23)),
             "health_func": grey_e_x_1, "perfect_item_func": perfect_sequence_1023},
            {"population_generator": BinomialPopulationGenerator(sequences_len=10,
                                                                 perfect_item=dec_to_grey(10.23, 0, 10.23)),
             "health_func": grey_e_x_2, "perfect_item_func": perfect_sequence_1023},
        ]

    for population_size in population_sizes:
        for param_set in params:
            population_generator = param_set["population_generator"]
            health_func = param_set["health_func"]
            perfect_item_func = param_set["perfect_item_func"]
            calc_noise = param_set.get("calc_noise", False)

            report_creator = ReportCreator(file_name, f"health func: {health_func.__name__}, "
                                                      f"sequences len: {population_generator.sequences_len}, "
                                                      f"population_size: {population_size}", calc_noise)

            for i in range(10):
                print(f"----------------------Iteration {i}----------------------")
                sequences = population_generator.generate_population(population_size=population_size)
                print("start population: ")
                sequences_with_health = [(i, health_func(i)) for i in sequences]

                if i == 0:
                    print_sequence_data(sequences_with_health, f"{type(population_generator).__name__} i: {i}, health_func: {health_func.__name__}")

                print("\n")

                print("Tournament With Return p=0.6")
                selection_class = TournamentWithReturnSelection(p=0.6)
                new_population, statistic = Evolution(sequences, health_func, perfect_item_func, selection_class, calc_noise,
                                                 draw_histogram=False).run_evolution()
                report_creator.save_statistics("tournament_with_return_p_0_6", statistic.copy())

                print("\n")

                print("Tournament With Return p=0.8")
                selection_class = TournamentWithReturnSelection(p=0.8)
                new_population, statistic = Evolution(sequences, health_func, perfect_item_func, selection_class,
                                                      calc_noise).run_evolution()
                report_creator.save_statistics("tournament_with_return_p_0_8", statistic.copy())
                print("\n")

                print("Tournament Without Return p=0.6")
                selection_class = TournamentWithoutReturnSelection(p=0.6)
                new_population, statistic = Evolution(sequences, health_func, perfect_item_func, selection_class,
                                                      calc_noise).run_evolution()
                report_creator.save_statistics("tournament_without_return_p_0_6", statistic.copy())
                print("\n")

                print("Tournament Without Return p=0.8")
                selection_class = TournamentWithoutReturnSelection(p=0.8)
                new_population, statistic = Evolution(sequences, health_func, perfect_item_func, selection_class,
                                                      calc_noise).run_evolution()
                report_creator.save_statistics("tournament_without_return_p_0_8", statistic.copy())
                print("\n")

                print("LinearRankingSelection b=1.6")
                selection_class = LinearRankingSelection(b=1.6)
                new_population, statistic = Evolution(sequences, health_func, perfect_item_func, selection_class,
                                                      calc_noise).run_evolution()
                report_creator.save_statistics("linear_ranking_selection_b_1_6", statistic.copy())
                print("\n")

                print("LinearRankingSelection b=1.2")
                selection_class = LinearRankingSelection(b=1.2)
                new_population, statistic = Evolution(sequences, health_func, perfect_item_func, selection_class,
                                                      calc_noise, draw_histogram=False).run_evolution()
                report_creator.save_statistics("linear_ranking_selection_b_1_2", statistic.copy())
                print("\n")

            report_creator.create_csv()


if __name__ == '__main__':
    main()
