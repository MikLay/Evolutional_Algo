import evolution_statistics

import matplotlib.pyplot as plt


def draw_histogram(population, title):
    health = [i[1] for i in population]

    # setting the ranges and no. of intervals
    range = (0, max(health))
    bins = 100

    # plotting a histogram
    plt.hist(health, bins, range, color='green',
             histtype='bar', rwidth=0.7)

    # x-axis label
    plt.xlabel('health')
    # frequency label
    plt.ylabel('% of individual')
    # plot title
    plt.title(title)

    # function to show the plot
    plt.show()


def draw_round_res(title, data_1, line_legend, data_2=None, line_legend_2=""):
    x = [i for i in range(len(data_1))]
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
    plt.show()