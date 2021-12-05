import numpy as np
import pickle


def main(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            xy1, xy2 = [xy.split(",") for xy in line.strip().split(" -> ")]
            xy1 = int(xy1[0]), int(xy1[1])
            xy2 = int(xy2[0]), int(xy2[1])
            lines.append([xy1, xy2])

    lines = np.array(lines)
    #np.save(open("lines.2.npy", "wb"), lines)
    #print(lines)

    N = lines.shape[0]
    imax, jmax = lines[:, :, 0].max(), lines[:, :, 1].max()
    grid = np.zeros((imax + 1, jmax + 1), np.int32)

    for l in range(N):
        p1, p2 = lines[l, 0, :], lines[l, 1, :]
        p1_ = np.minimum(p1, p2)
        p2_ = np.maximum(p1, p2)
        d12 = p2 - p1
        d = np.maximum(np.minimum(p2 - p1, 1), -1)
        num_pts = np.max(np.abs(d12)) + 1
        print(d12, num_pts, d)
        for m in range(num_pts):
            ij = p1 + m * d
            grid[ij[0], ij[1]] += 1

    print(grid.T)

    print((grid >= 2).sum())


if __name__ == "__main__":
    main("input.txt")
