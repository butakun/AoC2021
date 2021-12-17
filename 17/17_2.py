import numpy as np


def x_possible(v0x):
    return np.add.accumulate(np.arange(v0x, -1, -1))


def y_possible(v0y, ymin):
    vymin = -100
    while True:
        yy = np.add.accumulate(np.arange(v0y, vymin, -1))
        yy_ok = yy >= ymin
        if not np.all(yy_ok):
            return yy[yy_ok]
        vymin *= 2


def is_in_target(p, target):
    return np.all(p >= target[0, :]) and np.all(p <= target[1, :])


def is_past_target(p, v, target):
    if p[0] > target[1, 0] and v[0] >= 0:
        return True
    elif p[0] < target[0, 0] and v[0] <= 0:
        return True
    elif p[1] < target[0, 1] and v[1] <= 0:
        return True
    else:
        return False


def launch(p0, v0, target):
    p = np.array(p0)
    v = np.array(v0)
    reached = False
    y_top = p0[1]
    i_final = 0
    for i in range(100):
        p = p + v
        if abs(v[0]) > 0:
            v[0] = v[0] - v[0] / abs(v[0])
        v[1] = v[1] - 1
        reached = is_in_target(p, target)
        past = is_past_target(p, v, target)
        #print(i, p, v, reached, past)
        y_top = max(y_top, p[1])
        if reached or past:
            i_final = i - 1
            break

    return reached, i_final, y_top


def main(filename):
    if False:
        xmin, xmax = 20, 30
        ymin, ymax = -10, -5
    else:
        xmin, xmax = 241, 275
        ymin, ymax = -75, -49

    target = np.array([[xmin, ymin], [xmax, ymax]])

    vv0x = np.arange(21, 1000)
    vv0y = np.arange(-100, 1000)

    count = 0
    possibles = []
    for v0x in vv0x:
        xx = x_possible(v0x)
        xx_ok = np.logical_and(xx >= xmin, xx <= xmax)
        if not np.any(xx_ok):
            continue
        imax = xx.shape[0]

        for v0y in vv0y:
            yy = y_possible(v0y, ymin)
            jmax = yy.shape[0]

            yy_ok = np.logical_and(yy >= ymin, yy <= ymax)
            if not np.any(yy_ok):
                continue

            if jmax < imax:
                xx2 = xx[:jmax]
            else:
                xx2 = np.zeros_like(yy)
                xx2[:imax] = xx
                xx2[imax:] = xx[imax - 1]
            xx2_ok = np.logical_and(xx2 >= xmin, xx2 <= xmax)

            pp_ok = np.logical_and(xx2_ok, yy_ok)

            if np.any(pp_ok):
                possibles.append([v0x, v0y])
                count += 1
                print("v0 possible ", count, v0x, v0y, yy.max())

    print(f"{len(possibles)} possibles")

if __name__ == "__main__":
    main("input_debug.txt")
