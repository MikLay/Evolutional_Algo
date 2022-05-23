import os

import matplotlib.pyplot as plt

from helpers import grey_to_dec


def get_dir_name(conf, directory_name):
    health_func = conf["health_func"].__name__
    population_size = conf["population_size"]
    mutation = conf.get("mutation", 0)
    selection_method = conf["method"].name
    progin = conf["progin"] + 1
    mut_status = "with_mutation" if mutation > 0 else "without_mutation"

    dir_name = f'{directory_name}/{mut_status}/{health_func}/{population_size}/{selection_method}/{progin}'

    is_exist = os.path.exists(dir_name)
    if not is_exist:
        os.makedirs(dir_name)
    return dir_name


def default_genotype_phenotype_diagrams_q_10(population, conf, directory_name):
    default_genotype_phenotype_diagrams(population, conf, directory_name, 10)


def default_genotype_phenotype_diagrams_q_150(population, conf, directory_name):
    default_genotype_phenotype_diagrams(population, conf, directory_name, 150)


def default_genotype_phenotype_diagrams(population, conf, directory_name, q=1):
    health_func = conf["health_func"].__name__
    population_size = conf["population_size"]
    iter_num = conf.get("iter", 0)
    final = conf.get("final", False)
    final_text = 'Фінальна популяція' if final else ''

    # mut_status = "with_mutation" if mutation > 0 else "without_mutation"
    dir_name = get_dir_name(conf, directory_name)
    optimal_health = len(population[0][0]) * q

    health = [i[1] for i in population]
    distance_to_optimal = [(optimal_health - i[1]) for i in population]

    # phenotype
    bins = 100
    hist_range = (0, optimal_health)

    plt.figure()
    plt.hist(health, bins, hist_range, color='green',
             histtype='bar', rwidth=1)

    # x-axis label
    plt.xlabel('Health')
    # frequency label
    plt.ylabel('Num of individual')
    # plot title

    title = f"Розподіл здоров'я. Ф. здоров'я {health_func}, \n n = {population_size}, Ітерація {iter_num}. {final_text}"
    plt.title(title)

    plt.savefig(f"{dir_name}/Розподіл здоров'я, Ітерація {iter_num}, {final_text}.png")
    plt.close()

    # genotype
    plt.figure()
    plt.hist(distance_to_optimal, bins, hist_range, color='red',
             histtype='bar', rwidth=1)

    # x-axis label
    plt.xlabel('Distance to optimal')
    # frequency label
    plt.ylabel('Num of individual')
    # plot title

    title = f"Розподіл відстані до ідеальної. Ф. здоров'я {health_func}, \n n = {population_size}, Ітерація {iter_num}. {final_text}"
    plt.title(title)

    plt.savefig(f"{dir_name}/Розподіл відстані до ідеальної, Ітерація {iter_num}, {final_text}.png")
    plt.close()


def grey_0_1023_genotype_phenotype_diagrams(population, conf, directory_name):
    grey_genotype_phenotype_diagrams(population, conf, 0, 10.23, 10.23, directory_name=directory_name)


def grey_511_512_genotype_phenotype_diagrams(population, conf, directory_name):
    grey_genotype_phenotype_diagrams(population, conf, -5.11, 5.12, 0, directory_name=directory_name)


def grey_genotype_phenotype_diagrams(population, conf, a, b, optimal_x, directory_name):
    health_func = conf["health_func"].__name__
    population_size = conf["population_size"]
    iter_num = conf.get("iter", 0)
    final = conf.get("final", False)
    final_text = 'Фінальна популяція' if final else ''

    # mut_status = "with_mutation" if mutation > 0 else "without_mutation"
    dir_name = get_dir_name(conf, directory_name)

    # phenotype
    health = [i[1] for i in population]
    bins = 100

    plt.figure()
    plt.hist(health, bins, color='green',
             histtype='bar', rwidth=None)

    # x-axis label
    plt.xlabel('Health')
    # frequency label
    plt.ylabel('Num of individual')
    # plot title

    title = f"Розподіл здоров'я. Функція здоров'я {health_func}, n = {population_size}, \n Ітерація {iter_num}. {final_text}"
    plt.title(title)

    plt.savefig(f"{dir_name}/Розподіл здоров'я, Ітерація {iter_num}, {final_text}.png")
    plt.close()

    # genotype
    optimal_x = optimal_x
    x_values = [grey_to_dec(i[0], a, b) for i in population]
    bins = 100

    plt.figure()
    plt.hist(x_values, bins, color='red',
             histtype='bar', rwidth=None)

    # x-axis label
    plt.xlabel('X')
    # frequency label
    plt.ylabel('Num of individual')
    # plot title

    title = f"Значення X. Функція здоров'я {health_func}, n = {population_size}, \n Ітерація {iter_num}. {final_text}"
    plt.title(title)

    plt.savefig(f"{dir_name}/Значення X, Ітерація {iter_num}, {final_text}.png")
    plt.close()


def draw_round_res(params, data_1, line_legend, data_2=None, line_legend_2="", directory_name="RESULT"):
    health_func = params["health_func"].__name__
    population_size = params["population_size"]
    mutation = params.get("mutation", 0)
    selection_method = params["method"]
    progin = params["progin"] + 1

    title = f"Ф. здоров'я: {health_func},  Відбір: {selection_method}, \n Популяція: {population_size}, Прогін {progin}, P_мутації: {mutation}"

    x = [i for i in range(len(data_1))]
    plt.figure()
    plt.plot(x, data_1, label=line_legend)

    if data_2:
        plt.plot(x, data_2, label=line_legend_2)

    plt.xlabel('Номер популяції (ітерація)')
    if data_2:
        plt.ylabel(f'{line_legend}/{line_legend_2}')
    else:
        plt.ylabel(line_legend)
    plt.title(title)

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    mut_status = "with_mutation" if mutation > 0 else "without_mutation"
    file_title = line_legend
    if line_legend_2:
        file_title += f" + {line_legend_2}"
    dir_name = f'{directory_name}/{mut_status}/{health_func}/{population_size}/{selection_method}/{progin}'

    is_exist = os.path.exists(dir_name)
    if not is_exist:
        os.makedirs(dir_name)
    plt.savefig(f'{dir_name}/{file_title}.png')
    plt.close()