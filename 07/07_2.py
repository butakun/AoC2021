import numpy as np


def main(filename):
    with open(filename) as f:
        line = f.readline().strip()
        crabs = np.array([int(d) for d in line.split(",")])

    print(crabs)

    xmin, xmax = crabs.min(), crabs.max()
    targets = np.arange(xmin, xmax+1)
    dists = np.abs((crabs - targets[np.newaxis, :].T))
    fuels = (dists * (dists + 1) // 2).sum(axis=1)
    imin = np.argmin(fuels)
    print(targets[imin], fuels[imin])


if __name__ == "__main__":
    main("input.txt")
