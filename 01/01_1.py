import numpy as np


def main(filename):
    with open(filename) as f:
        depths = np.array([int(line) for line in f])

    delta = depths[1:] - depths[:-1]
    pm = delta > 0
    print(pm.sum())


if __name__ == "__main__":
    main("input.txt")
