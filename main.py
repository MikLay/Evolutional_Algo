from draw_diagrams import draw_health_distribution
from health_functions import fh
from init_sequences import init_normal


def main():
    sequences = init_normal(100, 100, "0"*100)
    for s in sequences:
        print(f"{s} \t health: {fh(s)}")
    draw_health_distribution(sequences, fh)


if __name__ == '__main__':
    main()
