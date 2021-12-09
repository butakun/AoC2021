import numpy as np

def main(filename):
    with open(filename) as f:
        heat = [[h for h in map(int, list(l.strip()))] for l in f]

    heat = np.array(heat)
    print(heat)

    imax, jmax = heat.shape
    print(imax, jmax)
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
                risk = heat[i, j] + 1
                print(i, j, heat[i, j], risk)
                total_risk += risk

    print(total_risk)

if __name__ == "__main__":
    main("input_debug_1.txt")
