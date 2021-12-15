import numpy as np
import heapq


class PrioritizedItem:
    def __init__(self, node, value):
        self.node = node
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value


def neighbors(grid, u):
    idim, jdim = grid.shape
    nei = []
    if u[0] > 0:
        nei.append((u[0] - 1, u[1]))
    if u[0] < idim - 1:
        nei.append((u[0] + 1, u[1]))
    if u[1] > 0:
        nei.append((u[0], u[1] - 1))
    if u[1] < jdim - 1:
        nei.append((u[0], u[1] + 1))
    return nei


def heuristic_func(grid, v):
    idim, jdim = grid.shape
    di = idim - 1 - v[0]
    dj = jdim - 1 - v[1]
    #return min(di, dj)
    return di + dj


def astar(grid, v1):
    inf = np.iinfo(np.int64).max
    idim, jdim = grid.shape

    open_set = [PrioritizedItem(v1, inf)]

    prev = np.zeros((grid.shape[0], grid.shape[1], 2), dtype=np.int64)
    F = np.zeros((grid.shape[0], grid.shape[1]), dtype=np.int64)
    G = np.zeros((grid.shape[0], grid.shape[1]), dtype=np.int64)

    F[:, :] = inf
    G[:, :] = inf

    G[v1[0], v1[1]] = 0
    F[v1[0], v1[1]] = heuristic_func(grid, v1)

    visited = 0
    while open_set:
        current = heapq.heappop(open_set).node
        visited += 1

        print("visiting ", current[0], current[1])
        if current[0] == idim - 1 and current[1] == jdim - 1:
            break

        nei = neighbors(grid, current)
        for v in nei:
            g_temp = G[current[0], current[1]] + grid[v[0], v[1]]
            if g_temp < G[v[0], v[1]]:
                prev[v[0], v[1], :] = current
                f = g_temp + heuristic_func(grid, v)
                G[v[0], v[1]] = g_temp
                F[v[0], v[1]] = f
                if v not in open_set:
                    heapq.heappush(open_set, PrioritizedItem(v, f))

    print("cost")
    print(G[idim - 1, jdim - 1])
    print("nodes visited ", visited)
    np.save(open("grid.npy", "wb"), grid)
    np.save(open("G.npy", "wb"), G)
    np.save(open("prev.npy", "wb"), prev)


def multiply_grid(grid):
    idim, jdim = grid.shape
    grid2 = np.zeros((5, 5, grid.shape[0], grid.shape[1]), np.int32)
    for gj in range(5):
        for gi in range(5):
            if gi > 0:
                subgrid = np.array(grid2[gi - 1, gj, :, :]) + 1
            elif gj > 0:
                subgrid = np.array(grid2[gi, gj - 1, :, :]) + 1
            else:
                subgrid = np.array(grid[:, :])

            subgrid[subgrid > 9] = 1
            grid2[gi, gj, :, :] = subgrid

    new_grid = np.zeros((5 * idim, 5 * jdim), np.int32)
    for gj in range(5):
        j0 = jdim * gj
        for gi in range(5):
            i0 = idim * gi
            new_grid[i0:i0+idim, j0:j0+jdim] = grid2[gi, gj, :, :]

    return new_grid


def main(filename):
    with open(filename) as f:
        grid = []
        for line in f:
            grid.append([int(v) for v in list(line.strip())])
        grid = np.array(grid)

    print(grid)

    gridL = multiply_grid(grid)

    astar(gridL, (0, 0))

if __name__ == "__main__":
    main("input.txt")
