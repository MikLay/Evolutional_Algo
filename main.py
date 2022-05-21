import statistics
from datetime import datetime

from draw_diagrams import default_genotype_phenotype_diagrams, grey_genotype_phenotype_diagrams, \
    grey_0_1023_genotype_phenotype_diagrams, grey_511_512_genotype_phenotype_diagrams, \
    default_genotype_phenotype_diagrams_q_150, default_genotype_phenotype_diagrams_q_10
from evolution import Evolution
from health_functions import fh, fhd_10, fhd_150, fconst, grey_x_2, grey_x, grey_x_4, grey_512_x_2, grey_512_x_4, \
    grey_512_x_2_get_x_by_y, grey_512_x_4_get_x_by_y, grey_x_get_x_by_y, grey_x_2_get_x_by_y, grey_x_4_get_x_by_y
from helpers import dec_to_grey
from init_sequences import BinomialPopulationGenerator, FConstPopulationGenerator, DecPopulationGenerator

# Варіант 10
# Турнірний стохастичний без повернення, t=2; p=0.6, p=0.8
# Турнірний стохастичний з поверненням, t=2; p=0.6, p=0.8
# За рангом лінійний, β=1.6, β=1.2
from successful_round_condition import f_const_successful_condition, fh_fhd_successful_condition, \
    grey_512_x_4_successful_condition, grey_512_x_2_successful_condition, grey_x_4_successful_condition, \
    grey_x_successful_condition, grey_x_2_successful_condition
from report_creator import ReportCreator
from selection_methods import TournamentWithReturnSelection, TournamentWithoutReturnSelection, LinearRankingSelection


def print_sequence_data(sequences_with_health, conf):
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
        sequences_health = [i[1] for i in sequences_with_health]
        print(f"sequence len: {len(sequences_with_health[0][0])}")
        print(f"population num: {len(sequences_health)}")
        print(f"max health: {max(sequences_health)}")
        print(f"min health: {min(sequences_health)}")
        print(f"statistics.mean health: {statistics.mean(sequences_health)}")


def run_evolution_for_config(conf, selection_classes, file_name, directory_name):
    population_generator = conf["population_generator"]
    health_func = conf["health_func"]
    successful_round_condition = conf["successful_round_condition"]
    calc_noise = conf.get("calc_noise", False)
    population_size = conf["population_size"]
    mutation = conf.get("mutation", 0)
    genotype_phenotype_diagrams = conf["genotype_phenotype_diagrams"]

    report_creator = ReportCreator(file_name, directory_name, conf, calc_noise)
    print(conf)
    for i in range(10):
        print(f"----------------------Iteration {i+1} ({datetime.now().time()}) ----------------------")
        if (mutation == 0) or (mutation > 0 and i < 5):
            add_perfect = True
        else:
            add_perfect = False
        sequences = population_generator.generate_population(population_size=population_size, add_perfect=add_perfect)
        sequences_with_health = [(i, health_func(i)) for i in sequences]

        if i == 0:
            print("start population: ")
            print_sequence_data(sequences_with_health, conf)
        for selection_class in selection_classes:
            print(f"{selection_class.name} ({datetime.now().time()})")
            new_population, statistic = Evolution(sequences, health_func, successful_round_condition, selection_class,
                                                  calc_noise, i, genotype_phenotype_diagrams, mutation, directory_name=directory_name).run_evolution()
            report_creator.save_statistics(selection_class.name, statistic.copy())
            print("\n")

    report_creator.create_csv()


def no_mutation_tests(file_name, directory_name):
    # population sizes
    # population_sizes = [100, 1000]
    population_sizes = [100]

    # health functions
    params = [
        # {"population_generator": FConstPopulationGenerator(sequences_len=100), "health_func": fconst,
        #  "successful_round_condition": f_const_successful_condition,
        #  "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams, "calc_noise": True},
        # {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fh,
        #  "successful_round_condition": fh_fhd_successful_condition,
        #  "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams},
        {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fhd_10,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams_q_10},
        {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fhd_150,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams_q_150},
        # {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_x_2_get_x_by_y,
        #                                                 x1=0, x2=10.23, y1=0, y2=(10.23**2), perfect_x=10.23),
        #  "health_func": grey_x_2, "successful_round_condition": grey_x_2_successful_condition,
        #  "genotype_phenotype_diagrams": grey_0_1023_genotype_phenotype_diagrams},
        # {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_x_get_x_by_y,
        #                                                 x1=0, x2=10.23, y1=0, y2=10.23, perfect_x=10.23),
        #  "health_func": grey_x, "successful_round_condition": grey_x_successful_condition,
        #  "genotype_phenotype_diagrams": grey_0_1023_genotype_phenotype_diagrams},
        # {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_x_4_get_x_by_y,
        #                                                 x1=0, x2=10.23, y1=0, y2=(10.23**4), perfect_x=10.23),
        #  "health_func": grey_x_4, "successful_round_condition": grey_x_4_successful_condition,
        #  "genotype_phenotype_diagrams": grey_0_1023_genotype_phenotype_diagrams},
        # {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_512_x_2_get_x_by_y,
        #                                                 x1=-5.11, x2=5.12, y1=0, y2=(5.12**2), perfect_x=0),
        #  "health_func": grey_512_x_2, "successful_round_condition": grey_512_x_2_successful_condition,
        #  "genotype_phenotype_diagrams": grey_511_512_genotype_phenotype_diagrams},
        # {"population_generator":  DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_512_x_4_get_x_by_y,
        #                                                 x1=-5.11, x2=5.12, y1=0, y2=(5.12**4), perfect_x=0),
        #  "health_func": grey_512_x_4, "successful_round_condition": grey_512_x_4_successful_condition,
        #  "genotype_phenotype_diagrams": grey_511_512_genotype_phenotype_diagrams},
    ]

    selection_classes = [
        TournamentWithReturnSelection(p=0.6), TournamentWithReturnSelection(p=0.8),
        TournamentWithoutReturnSelection(p=0.6), TournamentWithoutReturnSelection(p=0.8),
        LinearRankingSelection(b=1.6), LinearRankingSelection(b=1.2)
    ]

    for population_size in population_sizes:
        for param_set in params:
            param_set["population_size"] = population_size
            run_evolution_for_config(param_set, selection_classes, file_name, directory_name)


def ranking_mutation_tests(file_name, directory_name):
    ranking_configurations = [
        {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fh,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams,
         "population_size": 100, "mutation": 0.0000672757925523407},
        {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fhd_10,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams,
         "population_size": 100, "mutation": 0.0000660220531651611},
        {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_x_2_get_x_by_y,
                                                                x1=0, x2=10.23, y1=0, y2=(10.23**2), perfect_x=10.23),
            "health_func": grey_x_2, "successful_round_condition": grey_x_2_successful_condition,
            "genotype_phenotype_diagrams": grey_0_1023_genotype_phenotype_diagrams, "population_size": 100,
            "mutation": 0.00107915462143049},
        {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_512_x_2_get_x_by_y,
                                                                x1=-5.11, x2=5.12, y1=0, y2=(5.12**2), perfect_x=0),
            "health_func": grey_512_x_2, "successful_round_condition": grey_512_x_2_successful_condition,
            "genotype_phenotype_diagrams": grey_511_512_genotype_phenotype_diagrams, "population_size": 100,
         "mutation": 0.00107915462143049},

        # {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fh,
        #  "successful_round_condition": fh_fhd_successful_condition,
        #  "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams,
        #  "population_size": 1000, "mutation": 0.00000562050221292596},
        # {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fhd_10,
        #  "successful_round_condition": fh_fhd_successful_condition,
        #  "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams,
        #  "population_size": 1000, "mutation": 0.00000605962181613319},
        # {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_x_2_get_x_by_y,
        #                                                                 x1=0, x2=10.23, y1=0, y2=(10.23**2), perfect_x=10.23),
        #  "health_func": grey_x_2, "successful_round_condition": grey_x_2_successful_condition,
        #  "genotype_phenotype_diagrams": grey_0_1023_genotype_phenotype_diagrams, "population_size": 1000,
        #  "mutation": 0.000148257805588131},
        # {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_512_x_2_get_x_by_y,
        #                                                         x1=-5.11, x2=5.12, y1=0, y2=(5.12**2), perfect_x=0),
        #  "health_func": grey_512_x_2, "successful_round_condition": grey_512_x_2_successful_condition,
        #  "genotype_phenotype_diagrams": grey_511_512_genotype_phenotype_diagrams, "population_size": 1000,
        #  "mutation": 0.000148257805588131},
    ]

    selection_classes = [LinearRankingSelection(b=1.6), LinearRankingSelection(b=1.2)]

    for conf in ranking_configurations:
        run_evolution_for_config(conf, selection_classes, file_name, directory_name)


def tournament_mutation_tests(file_name, directory_name):
    ranking_configurations = [
        {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fh,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams,
         "population_size": 100, "mutation": 0.0000666318616569042},
        {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fhd_10,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams,
         "population_size": 100, "mutation": 0.0000520695589482784},
        {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_x_2_get_x_by_y,
                                                                                x1=0, x2=10.23, y1=0, y2=(10.23**2), perfect_x=10.23),
         "health_func": grey_x_2, "successful_round_condition": grey_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_0_1023_genotype_phenotype_diagrams, "population_size": 100,
         "mutation": 0.0011507972630316},
        {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_512_x_2_get_x_by_y,
                                                                        x1=-5.11, x2=5.12, y1=0, y2=(5.12**2), perfect_x=0),
         "health_func": grey_512_x_2, "successful_round_condition": grey_512_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_511_512_genotype_phenotype_diagrams, "population_size": 100,
         "mutation": 0.0011507972630316 },

        {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fh,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams,
         "population_size": 1000, "mutation": 0.00000640099968317935},
        {"population_generator": BinomialPopulationGenerator(sequences_len=100), "health_func": fhd_10,
         "successful_round_condition": fh_fhd_successful_condition,
         "genotype_phenotype_diagrams": default_genotype_phenotype_diagrams,
         "population_size": 1000, "mutation": 0.00000609314869128922},
        {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_x_2_get_x_by_y,
                                                                                x1=0, x2=10.23, y1=0, y2=(10.23**2), perfect_x=10.23),
         "health_func": grey_x_2, "successful_round_condition": grey_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_0_1023_genotype_phenotype_diagrams, "population_size": 1000,
         "mutation": 0.000148255878401541},
        {"population_generator": DecPopulationGenerator(sequences_len=10, get_x_by_y=grey_512_x_2_get_x_by_y,
                                                                        x1=-5.11, x2=5.12, y1=0, y2=(5.12**2), perfect_x=0),
         "health_func": grey_512_x_2, "successful_round_condition": grey_512_x_2_successful_condition,
         "genotype_phenotype_diagrams": grey_511_512_genotype_phenotype_diagrams, "population_size": 1000,
         "mutation": 0.000148255878401541},
    ]

    selection_classes = [TournamentWithReturnSelection(p=0.6), TournamentWithReturnSelection(p=0.8),
                         TournamentWithoutReturnSelection(p=0.6), TournamentWithoutReturnSelection(p=0.8)]

    for conf in ranking_configurations:
        run_evolution_for_config(conf, selection_classes, file_name, directory_name)


def main():
    file_name = "test_final_res.csv"
    directory_name = "test_FINAL_RES"
    no_mutation_tests(file_name, directory_name)
    # ranking_mutation_tests(file_name, directory_name)
    # tournament_mutation_tests(file_name, directory_name)


if __name__ == '__main__':
    main()
