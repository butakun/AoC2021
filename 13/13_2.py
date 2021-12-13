import numpy as np


def fold_grid(grid, fold):
    y_at, x_at = fold
    if y_at == 0:
        # fold along x
        folded = np.array(grid[:, :x_at])
        folded[:, :] = folded[:, :] | np.fliplr(grid[:, x_at + 1:])
    elif x_at == 0:
        # fold along y
        folded = np.array(grid[:y_at, :])
        folded[:, :] = folded[:, :] | np.flipud(grid[y_at + 1:, :])
    else:
        raise ValueError
    return folded


def main(filename):
    # grid[y, x]
    with open(filename) as f:
        dots = []
        for line in f:
            line = line.strip()
            if len(line) == 0:
                break
            tokens = line.strip().split(",")
            x, y = int(tokens[0]), int(tokens[1])
            dots.append([y, x])
        dots = np.array(dots)
        ymax = dots[:, 0].max()
        xmax = dots[:, 1].max()

        ydim, xdim = ymax + 1, xmax + 1

        folds = []
        for line in f:
            line = line.strip()
            equal = line.rfind("=")
            axis = line[equal-1]
            at = int(line[equal + 1:])
            if axis == "x":
                folds.append([0, at])
                xdim = max(xdim, at * 2 + 1)
            elif axis == "y":
                folds.append([at, 0])
                ydim = max(ydim, at * 2 + 1)
            else:
                raise ValueError(line)

        print("grid dim should be (ydim, xdim) = ", ydim, xdim)
        grid = np.zeros((ydim, xdim), bool)
        for dot in dots:
            grid[dot[0], dot[1]] = True


    print("grid shape = ", grid.shape)
    print(grid.astype(np.int32))
    print(folds)

    folded = np.array(grid)
    for fold in folds:
        folded = fold_grid(folded, fold)
        print("folded at ", fold)

    for line in folded:
        def dot(i):
            if i:
                return "*"
            else:
                return " "
        chars = [dot(c) for c in line]
        print("".join(chars))

if __name__ == "__main__":
    main("input.txt")
