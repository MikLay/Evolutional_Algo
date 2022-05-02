# from draw_diagrams import draw_health_distribution
import statistics

from draw_diagrams import draw_histogram
from evolution import Evolution
from health_functions import fh, fhd_10, fhd_50, fhd_150
from init_sequences import BinomialPopulationGenerator

# Варіант 10
# Турнірний стохастичний без повернення, t=2; p=0.6, p=0.8
# Турнірний стохастичний з поверненням, t=2; p=0.6, p=0.8
# За рангом лінійний, β=1.6, β=1.2
from report_creator import ReportCreator
from selection_methods import TournamentWithReturnSelection, TournamentWithoutReturnSelection, LinearRankingSelection


def print_sequence_data(sequences_with_health):
    print(sequences_with_health)
    sequences_health = [i[1] for i in sequences_with_health]
    # for s in sequences:
    #     print(f"{s} \t health: {fh(s)}")
    print(f"max health: {max(sequences_health)}")
    print(f"min health: {min(sequences_health)}")
    print(f"statistics.mean health: {statistics.mean(sequences_health)}")
    # draw_health_distribution(sequences, fh)


def main():
    sequences_len = 100
    population_size = 100
    params = [{"health_func": fh, "perfect_item": '0' * sequences_len},
              {"health_func": fhd_10, "perfect_item": '0' * sequences_len},
              {"health_func": fhd_50, "perfect_item": '0' * sequences_len},
              {"health_func": fhd_150, "perfect_item": '0' * sequences_len}]
    for param_set in params:
        health_func = param_set["health_func"]
        perfect_item = param_set["perfect_item"]
        report_creator = ReportCreator(f"report_{health_func.__name__}.csv")

        for i in range(10):
            print(f"----------------------Iteration {i}----------------------")
            sequences = BinomialPopulationGenerator(sequences_len=sequences_len).generate_population(population_size=population_size)
            print("start population: ")
            sequences_with_health = [(i, health_func(i)) for i in sequences]

            print_sequence_data(sequences_with_health)
            # draw_histogram(sequences_with_health)

            print("\n")

            print("Tournament With Return p=0.6")
            selection_class = TournamentWithReturnSelection(p=0.6)
            new_population, statistic = Evolution(sequences, health_func, perfect_item, selection_class,
                                             draw_histogram=False).run_evolution()
            report_creator.save_statistics("tournament_with_return_p_0_6", statistic.copy())

            print("\n")

            print("Tournament With Return p=0.8")
            selection_class = TournamentWithReturnSelection(p=0.8)
            new_population, statistic = Evolution(sequences, health_func, perfect_item, selection_class,
                                             ).run_evolution()
            report_creator.save_statistics("tournament_with_return_p_0_8", statistic.copy())
            print("\n")

            print("Tournament Without Return p=0.6")
            selection_class = TournamentWithoutReturnSelection(p=0.6)
            new_population, statistic = Evolution(sequences, health_func, perfect_item, selection_class,
                                             ).run_evolution()
            report_creator.save_statistics("tournament_without_return_p_0_6", statistic.copy())
            print("\n")

            print("Tournament Without Return p=0.8")
            selection_class = TournamentWithoutReturnSelection(p=0.8)
            new_population, statistic = Evolution(sequences, health_func, perfect_item, selection_class,
                                             ).run_evolution()
            report_creator.save_statistics("tournament_without_return_p_0_8", statistic.copy())
            print("\n")

            print("LinearRankingSelection b=1.6")
            selection_class = LinearRankingSelection(b=1.6)
            new_population, statistic = Evolution(sequences, health_func, perfect_item, selection_class,
                                             ).run_evolution()
            report_creator.save_statistics("linear_ranking_selection_b_1_6", statistic.copy())
            print("\n")

            print("LinearRankingSelection b=1.2")
            selection_class = LinearRankingSelection(b=1.2)
            new_population, statistic = Evolution(sequences, health_func, perfect_item, selection_class,
                                             draw_histogram=False).run_evolution()
            report_creator.save_statistics("linear_ranking_selection_b_1_2", statistic.copy())
            print("\n")

        report_creator.create_csv()


if __name__ == '__main__':
    main()
