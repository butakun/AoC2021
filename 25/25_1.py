import numpy as np


def dump(grid):
    for l in grid:
        print("".join(l.tolist()))


def step(grid):
    idim, jdim = grid.shape

    iorig, jorig = np.where(grid == '>')
    iadj, jadj = np.array(iorig), np.array(jorig)
    jadj += 1
    jadj[np.where(jadj >= jdim)] = 0

    canmovee = np.where(grid[iadj, jadj] == '.')[0]
    grid[iadj[canmovee], jadj[canmovee]] = '>'
    grid[iorig[canmovee], jorig[canmovee]] = '.'

    iorig, jorig = np.where(grid == 'v')
    iadj, jadj = np.array(iorig), np.array(jorig)
    iadj += 1
    iadj[np.where(iadj >= idim)] = 0

    canmoves = np.where(grid[iadj, jadj] == '.')[0]
    grid[iadj[canmoves], jadj[canmoves]] = 'v'
    grid[iorig[canmoves], jorig[canmoves]] = '.'

    return len(canmovee) + len(canmoves)


def main(filename):
    with open(filename) as f:
        grid = np.array([list(l.strip()) for l in f])

    i = 1
    while True:
        moved = step(grid)
        print(i, moved)
        if moved == 0:
            break
        i += 1

    dump(grid)

if __name__ == "__main__":
    main("input.txt")
