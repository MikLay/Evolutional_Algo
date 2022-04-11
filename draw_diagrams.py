import evolution_statistics

import matplotlib.pyplot as plt


def draw_histogram(population):
    health = [i[1] for i in population]

    # setting the ranges and no. of intervals
    range = (0, 100)
    bins = 100

    # plotting a histogram
    plt.hist(health, bins, range, color='green',
             histtype='bar', rwidth=0.7)

    # x-axis label
    plt.xlabel('health')
    # frequency label
    plt.ylabel('No. of individual')
    # plot title
    plt.title('Health Frequency')

    # function to show the plot
    plt.show()