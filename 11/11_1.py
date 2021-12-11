import numpy as np


def step(octs):
    imax, jmax = octs.shape

    octs[:, :] += 1
    flashed = np.zeros_like(octs, dtype=bool)
    while True:
        flash = octs[:, :] > 9
        if np.all(flash == False):
            break
        flash_inc = np.zeros_like(octs)
        flash_inc[flash] = 1

        octs[:-1, :] += flash_inc[1:, :]
        octs[1:, :]  += flash_inc[:-1, :]
        octs[:, :-1] += flash_inc[:, 1:]
        octs[:, 1:] += flash_inc[:, :-1]
        octs[:-1, :-1] += flash_inc[1:, 1:]
        octs[1:, 1:] += flash_inc[:-1, :-1]
        octs[:-1, 1:] += flash_inc[1:, :-1]
        octs[1:, :-1] += flash_inc[:-1, 1:]
        octs[flashed] = 0
        #print(flash)
        #print(flash_inc)
        octs[flash] = 0
        #print(octs)

        flashed = flashed | flash

    print(flashed)
    print(octs)
    return flashed


def main(filename):
    with open(filename) as f:
        octs = np.array([[int(c) for c in list(l.strip())] for l in f])

    print(octs)
    acc = 0
    for i in range(100):
        print("step ", i + 1)
        flashed = step(octs)
        print("flashed = ", flashed.sum())
        acc += flashed.sum()

    print(acc)

if __name__ == "__main__":
    main("input.txt")
