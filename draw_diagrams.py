import os

import matplotlib.pyplot as plt

RESULT_DIR_NAME = "FINAL_RES_M"


def draw_histogram(population, conf):
    global RESULT_DIR_NAME

    health_func = conf["health_func"].__name__
    population_size = conf["population_size"]
    mutation = conf.get("mutation", 0)
    iter = conf.get("iter", 0)
    selection_method = conf["method"].name
    progin = conf["progin"] + 1
    final = conf.get("final", False)

    health = [i[1] for i in population]

    # setting the ranges and no. of intervals
    range = (0, max(health))
    bins = 100

    plt.figure()
    # plotting a histogram
    plt.hist(health, bins, range, color='green',
             histtype='bar', rwidth=0.7)

    # x-axis label
    plt.xlabel('health')
    # frequency label
    plt.ylabel('Num of individual')
    # plot title
    final_text ='Фінальна популяція' if final else ''
    title = f"Функція здоров'я {health_func}, розмір популяції {population_size}, \n Ітерація {iter}. {final_text}"
    plt.title(title)

    mut_status = "with_mutation" if mutation > 0 else "without_mutation"
    dir_name = f'{RESULT_DIR_NAME}/{mut_status}/{health_func}/{population_size}/{selection_method}/{progin}'

    is_exist = os.path.exists(dir_name)
    if not is_exist:
        os.makedirs(dir_name)
    plt.savefig(f"{dir_name}/Розподіл здоров'я в популяції, Ітерація {iter}, {final_text}.png")
    plt.close()


def draw_round_res(params, data_1, line_legend, data_2=None, line_legend_2=""):
    global RESULT_DIR_NAME

    health_func = params["health_func"].__name__
    population_size = params["population_size"]
    mutation = params.get("mutation", 0)
    selection_method = params["method"]
    progin = params["progin"] + 1

    title = f"Ф. здоров'я: {health_func}, Популяції: {population_size}, \n Відбір: {selection_method}, Прогін {progin}, P_мутації: {mutation}"

    x = [i for i in range(len(data_1))]
    plt.figure()
    plt.plot(x, data_1, label=line_legend)

    if data_2:
        plt.plot(x, data_2, label=line_legend_2)

    plt.xlabel('population num')
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
    dir_name = f'{RESULT_DIR_NAME}/{mut_status}/{health_func}/{population_size}/{selection_method}/{progin}'

    is_exist = os.path.exists(dir_name)
    if not is_exist:
        os.makedirs(dir_name)
    plt.savefig(f'{dir_name}/{file_title}.png')
    plt.close()