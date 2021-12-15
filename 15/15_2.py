import numpy as np


def dijkstra(grid, v1):
    dist = np.zeros((grid.shape[0], grid.shape[1]), dtype=np.int32)
    visited = np.zeros_like(grid, dtype=bool)
    prev = np.zeros((grid.shape[0], grid.shape[1], 2), dtype=np.int32)

    inf = np.iinfo(np.int32).max
    dist[:, :] = inf
    visited[:, :] = False
    prev[:, :] = (0, 0)

    dist[v1[0], v1[1]] = 0

    idim, jdim = grid.shape
    Q = [(i, j) for i in range(idim) for j in range(jdim)]
    print(Q)

    while Q:
        u = Q[0]
        min_dist = dist[u[0], u[1]]
        for i, j in Q:
            if dist[i, j] < min_dist:
                min_dist = dist[i, j]
                u = (i, j)
        Q.remove(u)
        print(u, min_dist)

        if u[0] == idim - 1 and u[1] == jdim - 1:
            break

        nei = []
        if u[0] > 0:
            nei.append((u[0] - 1, u[1]))
        if u[0] < idim - 1:
            nei.append((u[0] + 1, u[1]))
        if u[1] > 0:
            nei.append((u[0], u[1] - 1))
        if u[1] < jdim - 1:
            nei.append((u[0], u[1] + 1))

        for v in nei:
            if visited[v[0], v[1]]:
                continue

            alt = dist[u[0], u[1]] + grid[v[0], v[1]]
            if alt < dist[v[0], v[1]]:
                dist[v[0], v[1]] = alt
                prev[v[0], v[1]] = u

            visited[v[0], v[1]] = True

    print(u, dist[u[0], u[1]])


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


def funcH(grid, v):
    idim, jdim = grid.shape
    di = idim - 1 - v[0]
    dj = jdim - 1 - v[1]
    return di + dj


def astar(grid, v1):
    idim, jdim = grid.shape

    open_set = [v1]
    prev = np.zeros((grid.shape[0], grid.shape[1], 2), dtype=np.int64)
    F = np.zeros((grid.shape[0], grid.shape[1]), dtype=np.int64)
    G = np.zeros((grid.shape[0], grid.shape[1]), dtype=np.int64)

    inf = np.iinfo(np.int64).max
    F[:, :] = inf
    G[:, :] = inf

    G[v1[0], v1[1]] = 0
    F[v1[0], v1[1]] = funcH(grid, v1)

    while open_set:

        current = open_set[-1]
        min_f = F[current[0], current[1]]
        for c in open_set:
            f = F[c[0], c[1]]
            if f < min_f:
                current = c
                min_f = f
        open_set.remove(current)

        print("a* ", current)
        if current[0] == idim - 1 and current[1] == jdim - 1:
            break

        nei = neighbors(grid, current)
        for v in nei:
            g_temp = G[current[0], current[1]] + grid[v[0], v[1]]
            if g_temp < G[v[0], v[1]]:
                prev[v[0], v[1], :] = current
                G[v[0], v[1]] = g_temp
                F[v[0], v[1]] = g_temp + funcH(grid, v)
                if v not in open_set:
                    open_set.append(v)

    print("cost")
    print(G[idim - 1, jdim - 1])

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
