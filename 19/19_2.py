import numpy as np
import pickle

L = 1000
M = 2 * L + 1


def invert_rot(rot):
    inv = [None, None, None]
    for i in [0, 1, 2]:
        inv[abs(rot[i]) - 1] = rot[i] // abs(rot[i]) * (i + 1)
    return inv


def invert(rot, d):
    rot_inv = invert_rot(rot)

    d_inv = [None, None, None]
    for i in [0, 1, 2]:
        d_inv[abs(rot_inv[i]) - 1] = -rot_inv[i] // abs(rot_inv[i]) * d[i]
    return rot_inv, d_inv


def orient_a_beacon(ijk2, rot, d2_1=[0,0,0]):
    ijk2_1 = np.array([0, 0, 0])
    for l2 in [0, 1, 2]:
        di = rot[l2] // abs(rot[l2])
        l1 = abs(rot[l2]) - 1
        ijk2_1[l1] = di * ijk2[l2] + d2_1[l1]
    return ijk2_1


def orient_beacons_old(beacons2, rot, d2_1):
    beacons2_1 = []
    for i, ijk2 in enumerate(beacons2):
        ijk2_1 = orient_a_beacon(ijk2, rot, d2_1)
        beacons2_1.append(ijk2_1)
        #print(f"  {ijk2} -> {ijk2_1}")
    return np.array(beacons2_1)


def orient_beacons(beacons2, rot, d2_1):
    l1 = [None, None, None]
    di = [None, None, None]
    for l2 in [0, 1, 2]:
        di[l2] = rot[l2] // abs(rot[l2])
        l1[l2] = abs(rot[l2]) - 1

    beacons2_1 = np.zeros_like(beacons2)
    beacons2_1[:, l1[0]] = di[0] * beacons2[:, 0]
    beacons2_1[:, l1[1]] = di[1] * beacons2[:, 1]
    beacons2_1[:, l1[2]] = di[2] * beacons2[:, 2]
    beacons2_1 += d2_1
    return beacons2_1


def match_beacons(beacons1, beacons2_1):
    match = []

    inrange = np.logical_not(np.any(np.abs(beacons2_1) > 1000, axis=1))
    beacons2_1_ = beacons2_1[inrange]
    orig_indices = np.where(inrange)[0]

    for i, beacon1 in enumerate(beacons1):
        for j, beacon2 in enumerate(beacons2_1_):
            d = beacon2 - beacon1 
            if np.all(d == 0):
                match.append((i, orig_indices[j]))
    return np.array(match)


def find_transform_path(iscanner, mapping):
    assert iscanner != 0

    def dfs(i, path, mapping):
        path.append(i)
        if 0 in mapping[i]:
            path.append(0)
            return True
        else:
            for j in mapping[i].keys():
                if j in path:
                    continue
                if dfs(j, path, mapping):
                    return True
            path.pop()
        return False

    path = []
    dfs(iscanner, path, mapping)
    return path


def main(filename):
    with open(filename) as f:
        scanners = []
        for line in f:
            tokens = line.strip().split()
            assert tokens[1] == "scanner"
            beacons = []
            for line in f:
                xyz = line.strip().split(",")
                if len(xyz) < 3:
                    break
                xyz = int(xyz[0]), int(xyz[1]), int(xyz[2])
                beacons.append(xyz)
            scanners.append(np.array(beacons, dtype=np.int32))

    n_scanners = len(scanners)

    mapping = pickle.load(open("mapping.1.pkl", "rb"))
    print("mapping ")
    for k, v in mapping.items():
        print(f"{k}: ")
        for k2, v2 in v.items():
            print(f"  {k2}: {v2[1]}, {v2[2]}")

    paths = {}
    uniques = set()
    positions = {}
    for iscanner, beacons in enumerate(scanners):
        if iscanner == 0:
            positions[iscanner] = np.array([0, 0, 0])
            continue

        print("iscanner  =", iscanner)
        path = find_transform_path(iscanner, mapping)
        print("  path =", path)
        i_from = path.pop(0)
        p = np.array([0, 0, 0])
        while path:
            i_to = path.pop(0)
            _, rot, d = mapping[i_from][i_to]
            p = orient_a_beacon(p, rot, d)
            print(p)
            i_from = i_to
        positions[iscanner] = p

    print(positions)

    dists = []
    for i in range(n_scanners):
        pi = positions[i]
        for j in range(i + 1, n_scanners):
            pj = positions[j]
            dist = np.abs(pj - pi).sum()
            print(f"Dist {i} - {j} = {dist}")
            dists.append(np.abs(pj - pi).sum())

    dists = np.array(dists)
    print("max = ", dists.max())


if __name__ == "__main__":
    main("input.txt")
