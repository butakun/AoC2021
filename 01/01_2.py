import numpy as np


def main(filename):
    with open(filename) as f:
        depths = np.array([int(line) for line in f])

    sliding_average = (depths[:-2] + depths[1:-1] + depths[2:]) / 3.0
    delta = sliding_average[1:] - sliding_average[:-1]
    pm = delta > 0
    print(pm.sum())


if __name__ == "__main__":
    main("input.txt")
