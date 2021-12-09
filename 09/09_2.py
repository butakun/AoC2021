import numpy as np


def find_low_points(heat):

    low_points = []
    imax, jmax = heat.shape
    total_risk = 0
    for i in range(imax):
        im = max(0, i - 1)
        ip = min(imax - 1, i + 1)
        for j in range(jmax):
            jm = max(0, j - 1)
            jp = min(jmax - 1, j + 1)
            if i < imax - 1:
                down = heat[i, j] < heat[ip, j]
            else:
                down = True
            if i > 0:
                up = heat[i, j] < heat[im, j]
            else:
                up = True
            if j < jmax - 1:
                left = heat[i, j] < heat[i, jp]
            else:
                left = True
            if j > 0:
                right = heat[i, j] < heat[i, jm]
            else:
                right = True
            low = up and down and left and right
            if low:
                low_points.append([i, j])
    return low_points


def find_basin(heat, i0, j0):
    def nei(i, j, imax, jmax):
        n = []
        if i < imax - 1:
            n.append([i + 1, j])
        if i > 0:
            n.append([i - 1, j])
        if j < jmax - 1:
            n.append([i, j + 1])
        if j > 0:
            n.append([i, j - 1])
        return n

    imax, jmax = heat.shape

    done = set()
    def dfs(i, j):
        done.add((i, j))
        basin_nei = []
        for ii, jj in nei(i, j, imax, jmax):
            uphill = heat[ii, jj] > heat[i, j] and heat[ii, jj] < 9
            if uphill:
                #print(f"{ii}, {jj} ({heat[ii,jj]} < {i}, {j} ({heat[i,j]})")
                basin_nei.append((ii, jj))
        for ii, jj in basin_nei:
            if (ii, jj) not in done:
                dfs(ii, jj)

    dfs(i0, j0)
    return done


def main(filename):
    with open(filename) as f:
        heat = [[h for h in map(int, list(l.strip()))] for l in f]

    heat = np.array(heat)
    print(heat)

    low_points = find_low_points(heat)
    print(low_points)

    sizes = []
    for i, j in low_points:
        basin = find_basin(heat, i, j)
        print(f"basin {i}, {j}, size {len(basin)}")
        sizes.append(len(basin))
    print(sizes)

    res = sorted(sizes, reverse=True)
    res = res[0] * res[1] * res[2]
    print(res)

if __name__ == "__main__":
    main("input.txt")
