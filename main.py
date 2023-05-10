import statistics
import sys
from datetime import datetime
from collections import Counter

from draw_diagrams import default_genotype_phenotype_diagrams, \
    grey_0_1023_genotype_phenotype_diagrams, grey_511_512_genotype_phenotype_diagrams, \
    default_genotype_phenotype_diagrams_q_150, default_genotype_phenotype_diagrams_q_10, \
    default_genotype_phenotype_diagrams_q_100
from evolution import Evolution
from health_functions import fh, fhd_10, fhd_150, fconst, grey_x_2, grey_x, grey_x_4, grey_512_x_2, grey_512_x_4, \
    grey_512_x_2_get_x_by_y, grey_512_x_4_get_x_by_y, grey_x_get_x_by_y, grey_x_2_get_x_by_y, grey_x_4_get_x_by_y, \
    fhd_100, grey_e_x_025, grey_e_x_1, grey_e_x_2
from init_sequences import BinomialPopulationGenerator, FConstPopulationGenerator, DecPopulationGenerator

# Варіант 9
# Турнірний стохастичний без повернення, t=2; p=0.95; p=0.9; p=0.8; p=0.75
# Турнірний стохастичний з поверненням, t=2; p=0.95; p=0.9; p=0.8; p=0.75


from successful_round_conditions import f_const_successful_condition, fh_fhd_successful_condition, \
    grey_512_x_4_successful_condition, grey_512_x_2_successful_condition, grey_x_4_successful_condition, \
    grey_x_successful_condition, grey_x_2_successful_condition
from report_creator import ReportCreator
from selection_methods import TournamentWithReturnSelection, TournamentWithoutReturnSelection, LinearRankingSelection


def print_sequence_data(sequences_with_health, conf):
    if sequences_with_health:
        # print sequence and draw diagram
        # print(sequences_with_health)
        seq_freq = Counter(seq for seq, _ in sequences_with_health)
        for seq, count in seq_freq.items():
            print(seq, count)
        sequences_health = [i[1] for i in sequences_with_health]
        print(f"sequence len: {len(sequences_with_health[0][0])}")
        print(f"population num: {len(sequences_health)}")
        print(f"max health: {max(sequences_health)}")
        print(f"min health: {min(sequences_health)}")
        print(f"statistics.mean health: {statistics.mean(sequences_health)}")
        print(f"Mutation: {conf.get('mutation_p', 0)}")
        print(f"Crossover: {conf.get('crossover', False)}")


def run_evolution_for_config(conf, selection_classes, file_name, directory_name):
    # population_generator = conf["population_generator"]
    health_func = conf["health_func"]
    successful_round_condition = conf["successful_round_condition"]
    calc_noise = conf.get("calc_noise", False)
    populations = conf.get("populations",[])
    # population_size = conf["population_size"]
    mutation = conf.get("mutation", False)
    mutation_p = conf.get("mutation_p", 0)
    crossover = conf.get("crossover", False)
    genotype_phenotype_diagrams = conf["genotype_phenotype_diagrams"]

    # Rewrite mutation value
    report_creator = ReportCreator(file_name, directory_name, conf, calc_noise)
    for i in range(len(populations)):
        print(f"----------------------Iteration {i+1} ({datetime.now().time()}) ----------------------")
        sequences = populations[i]
        sequences_with_health = [(i, health_func(i)) for i in sequences]

        if i == 0:
            print("Start population: ")
            print_sequence_data(sequences_with_health, conf)
        for selection_class in selection_classes:
            print(f"{selection_class.name} ({datetime.now().time()})")
            new_population, statistic = Evolution(sequences, health_func, successful_round_condition, selection_class,
                                                  calc_noise, i, genotype_phenotype_diagrams, mutation, mutation_p, crossover, directory_name=directory_name).run_evolution()
            report_creator.save_statistics(selection_class.name, statistic.copy())
            print("\n")

    report_creator.create_csv()

def mutation_tests(file_name, directory_name, population_size=100, iterations=100):
    print('----------------------------------------------------------------------------------------------------')
    print(f'---- Experiment started.  population_size={population_size}, iterations={100}, encoding=Grey ----')
    print('----------------------------------------------------------------------------------------------------')
    fconst_generator = FConstPopulationGenerator(sequences_len=100)
    binominal_fhd_100 = BinomialPopulationGenerator(sequences_len=100, x1=0, x2=1, perfect_x=0)
    binominal_grey_x_2 = BinomialPopulationGenerator(sequences_len=10, x1=0, x2=10.23, perfect_x=10.23)
    binominal_grey_512_x_2 = BinomialPopulationGenerator(sequences_len=10, x1=-5.11, x2=5.12, perfect_x=0)

    # For No_mutation/Mutation/Crossover/M+C
    fconst_populations = [fconst_generator.generate_population(population_size) for _ in range(iterations)]
    fhd_100_populations = [binominal_fhd_100.generate_population(population_size) for _ in range(iterations)]
    grey_x_2_populations = [binominal_grey_x_2.generate_population(population_size) for _ in range(iterations)]
    grey_512_x_2_populations = [binominal_grey_512_x_2.generate_population(population_size) for _ in range(iterations)]

    mutation_100 = 0.1/100/population_size
    mutation_10 = 0.1/10/population_size

    # health functions
    params = [
        # FConstAll
        {"populations": fconst_populations.copy(),
         "health_func": fconst,
         "successful_round_condition": f_const_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams,
         "calc_noise": True
         },
        # FHD q=100 without mutations
        {"populations": fhd_100_populations.copy(),
         "health_func": fhd_100,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams_q_100
         },
        # FHD q=100 with mutations
        {"populations": fhd_100_populations.copy(),
         "health_func": fhd_100,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams_q_100,
         "mutation": True,
         "mutation_p": mutation_100
         },
        # FHD q=100 crossover
        {"populations": fhd_100_populations.copy(),
         "health_func": fhd_100,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams_q_100,
         "mutation": False,
         "crossover": True,
         "mutation_p": 0
         },
        # FHD q=100 M+C
        {"populations": fhd_100_populations.copy(),
         "health_func": fhd_100,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams_q_100,
         "mutation": True,
         "crossover": True,
         "mutation_p": mutation_100
         },
        # f(x)  степенева:
        # y=x^2, 0≤x≤10.23 . Глобальний максимум:  y=〖(10.23)〗^2,  x=10.23.
        {"populations": grey_x_2_populations.copy(),
         "health_func": grey_x_2,
         "successful_round_condition": grey_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_0_1023_genotype_phenotype_diagrams
         },
        # Mutation
        {"populations": grey_x_2_populations.copy(),
         "health_func": grey_x_2,
         "successful_round_condition": grey_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_0_1023_genotype_phenotype_diagrams,
         "mutation": True,
         "mutation_p": mutation_10
         },
        # Crossover
        {"populations": grey_x_2_populations.copy(),
         "health_func": grey_x_2,
         "successful_round_condition": grey_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_0_1023_genotype_phenotype_diagrams,
         "mutation": False,
         "crossover": True,
         "mutation_p": 0
         },
        # M+C
        {"populations": grey_x_2_populations.copy(),
         "health_func": grey_x_2,
         "successful_round_condition": grey_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_0_1023_genotype_phenotype_diagrams,
         "mutation": True,
         "crossover": True,
         "mutation_p": mutation_10
         },
        # y=〖(5.12)〗^2-x^2,   -5.12≤x<5.12 Глобальний максимум:  y=〖(5.12)〗^2,x=0.
        {"populations": grey_512_x_2_populations.copy(),
         "health_func": grey_512_x_2,
         "successful_round_condition": grey_512_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_511_512_genotype_phenotype_diagrams,
         },
        # Mutation
        {"populations": grey_512_x_2_populations.copy(),
         "health_func": grey_512_x_2,
         "successful_round_condition": grey_512_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_511_512_genotype_phenotype_diagrams,
         "mutation": True,
         "mutation_p": mutation_10
         },
        # Crossover
        {"populations": grey_512_x_2_populations.copy(),
         "health_func": grey_512_x_2,
         "successful_round_condition": grey_512_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_511_512_genotype_phenotype_diagrams,
         "mutation": False,
         "crossover": True,
         "mutation_p": 0
         },
        # M + C
        {"populations": grey_512_x_2_populations.copy(),
         "health_func": grey_512_x_2,
         "successful_round_condition": grey_512_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_511_512_genotype_phenotype_diagrams,
         "mutation": True,
         "crossover": True,
         "mutation_p": mutation_10
         },

    ]

    selection_classes = [
        TournamentWithReturnSelection(p=2),
        TournamentWithReturnSelection(p=0.95),
        TournamentWithReturnSelection(p=0.9),
        TournamentWithReturnSelection(p=0.8),
        TournamentWithReturnSelection(p=0.75),
        TournamentWithoutReturnSelection(p=2),
        TournamentWithoutReturnSelection(p=0.95),
        TournamentWithoutReturnSelection(p=0.9),
        TournamentWithoutReturnSelection(p=0.8),
        TournamentWithoutReturnSelection(p=0.75)]

    for param_set in params:
        param_set['population_size'] = population_size
        run_evolution_for_config(param_set, selection_classes, file_name, directory_name)

def main():
    file = open('output.txt', 'a')
    sys.stdout = file
    file_name = "results.csv"
    directory_name = "RESULTS"
    mutation_tests(file_name, directory_name, population_size=100, iterations=100)
    # mutation_tests(file_name, directory_name, population_size=200, iterations=100)
    # mutation_tests(file_name, directory_name, population_size=300, iterations=100)
    # mutation_tests(file_name, directory_name, population_size=400, iterations=100)
    # mutation_tests(file_name, directory_name, population_size=500, iterations=100)
    file.close()


if __name__ == '__main__':
    main()
