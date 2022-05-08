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