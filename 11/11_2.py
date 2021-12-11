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
    num_octs = octs.shape[0] * octs.shape[1]
    i = 0
    while True:
        print("step ", i + 1)
        flashed = step(octs)
        print("flashed = ", flashed.sum())
        if flashed.sum() == num_octs:
            print("all flashed, at step ", i + 1)
            break

        i += 1

if __name__ == "__main__":
    main("input.txt")
