from draw_diagrams import draw_health_distribution
from evolution import Evolution
from health_functions import fh
from init_sequences import BinomialPopulationGenerator


# Варіант 10
# Турнірний стохастичний без повернення, t=2; p=0.6, p=0.8
# Турнірний стохастичний з поверненням, t=2; p=0.6, p=0.8
# За рангом лінійний, β=1.6, β=1.2
from selection_methods import tournament_without_return, tournament_with_return


def main():
    sequences = BinomialPopulationGenerator(sequences_len=100).generate_population(population_size=100)
    for s in sequences:
        print(f"{s} \t health: {fh(s)}")
    # draw_health_distribution(sequences, fh)
    print("================================")
    new_population = Evolution(sequences, fh, tournament_with_return, additional_params={"p": 0.6}).run_evolution()
    for s in new_population:
        print(f"{s} \t health: {fh(s)}")
    print("================================")
    new_population = Evolution(sequences, fh, tournament_without_return, additional_params={"p": 0.6}).run_evolution()
    for s in new_population:
        print(f"{s} \t health: {fh(s)}")


if __name__ == '__main__':
    main()
