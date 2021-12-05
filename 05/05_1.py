import numpy as np
import pickle


def main(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            xy1, xy2 = [xy.split(",") for xy in line.strip().split(" -> ")]
            xy1 = int(xy1[0]), int(xy1[1])
            xy2 = int(xy2[0]), int(xy2[1])
            if xy1[0] == xy2[0] or xy1[1] == xy2[1]:
                lines.append([xy1, xy2])

    lines = np.array(lines)
    np.save(open("lines.npy", "wb"), lines)
    print(lines)

    N = lines.shape[0]
    imax, jmax = lines[:, :, 0].max(), lines[:, :, 1].max()
    grid = np.zeros((imax + 1, jmax + 1), np.int32)

    for l in range(N):
        p1, p2 = lines[l, 0, :], lines[l, 1, :]
        print("line: ", p1, p2)
        p1_ = np.minimum(p1, p2)
        p2_ = np.maximum(p1, p2)
        for i in range(p1_[0], p2_[0] + 1):
            for j in range(p1_[1], p2_[1] + 1):
                print(i, j)
                grid[i, j] += 1

    print(grid)

    print((grid >= 2).sum())


if __name__ == "__main__":
    main("input.txt")
