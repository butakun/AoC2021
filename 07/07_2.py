import numpy as np


def main(filename):
    with open(filename) as f:
        line = f.readline().strip()
        crabs = np.array([int(d) for d in line.split(",")])

    print(crabs)

    xmin, xmax = crabs.min(), crabs.max()

    fuels = np.zeros((xmax - xmin + 1, 2))
    x_fuel_min = None
    fuel_min = None
    for x in range(xmin, xmax + 1):
        dists = np.abs(crabs - x)
        for i, d in enumerate(dists):
                dists[i] = np.arange(1, d+1).sum()
        fuel = dists.sum()
        print(x, fuel)

        if x_fuel_min is None:
            x_fuel_min = x
            fuel_min = fuel
        else:
            if fuel < fuel_min: 
                x_fuel_min = x
                fuel_min = fuel

    print(x_fuel_min, fuel_min)


if __name__ == "__main__":
    main("input.txt")
