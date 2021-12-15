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


def main(filename):
    with open(filename) as f:
        grid = []
        for line in f:
            grid.append([int(v) for v in list(line.strip())])
        grid = np.array(grid)

    print(grid)

    dijkstra(grid, (0, 0))

if __name__ == "__main__":
    main("input.txt")
