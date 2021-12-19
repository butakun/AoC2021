import numpy as np
import pickle

L = 1000
M = 2 * L + 1

# map2's xyz can map to map1's xyz as:
ROTS = [
    (1, 2, 3), (1, 3, -2), (1, -2, -3), (1, -3, 2),
    (2, 1, -3), (2, -3, -1), (2, -1, 3), (2, 3, 1),
    (3, 1, 2), (3, 2, -1), (3, -1, -2), (3, -2, 1),
    (-1, 2, -3), (-1, -3, -2), (-1, -2, 3), (-1, 3, 2),
    (-2, 1, 3), (-2, -3, 1), (-2, -1, -3), (-2, 3, -1),
    (-3, 1, -2), (-3, -2, -1), (-3, -1, 2), (-3, 2, 1),
    ]


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


def debug_1():
    rot = ROTS[0]
    beacons1 = np.array([[2, 2, 0], [3, 4, 0]])
    beacons2 = np.array([[0, 0, 0], [1, 2, 0]])
    p1 = beacons1[0]
    p2 = beacons2[0]
    d = p1 - orient_a_beacon(p2, rot)
    beacons2_1 = orient_beacons(beacons2, rot, d)
    match = match_beacons(beacons1, beacons2_1)
    print(match)
    return


def debug_3(scanners):
    beacons1 = scanners[1]
    beacons2 = scanners[4]

    rot = (-3, 1, -2)
    beacon1 = beacons1[13]
    beacon2 = beacons2[1]

    d = beacon1 - orient_a_beacon(beacon2, rot)
    beacons2_1 = orient_beacons(beacons2, rot, d)

    match = match_beacons(beacons1, beacons2_1)
    if len(match) >= 12:
        print(f"  matched ", len(match), " rot = ", rot, d) 
        print(match)
        matched = True

def debug_4(scanners):
    beacons1, beacons2 = scanners[0], scanners[1]
    match, rot, d = compare_scanners(beacons1, beacons2)
    beacons2_1 = orient_beacons(beacons2, rot, d)

    for i, j in match:
        beacon1, beacon2, beacon2_1 = beacons1[i], beacons2[j], beacons2_1[j]
        print(f"{i}:{j}: {beacon1} {beacon2} {beacon2_1}")


def debug_5():
    mapping = {
            0:{1:"A"}, 1:{0:"A", 3:"B", 4:"C"},
            2:{4:"D"},
            3:{1:"B"},
            4:{1:"C", 2:"D"},
            }

    for i in range(1, 5):
        path = find_transform_path(i, mapping)
        print(path)


def debug_6():
    mapping = pickle.load(open("mapping_debug.pkl", "rb"))

    path = find_transform_path(2, mapping)
    print(path)
    _, rot24, d24 = mapping[2][4]
    print("2->4: ", rot24, d24)
    _, rot41, d41 = mapping[4][1]
    print("4->1: ", rot41, d41)
    _, rot10, d10 = mapping[1][0]
    print("1->0: ", rot10, d10)

    o = orient_a_beacon([0, 0, 0], rot24, d24)
    print("2 -> 4: ", o)
    o = orient_a_beacon(o, rot41, d41)
    print("4 -> 1: ", o)
    o = orient_a_beacon(o, rot10, d10)
    print("1 -> 0: ", o)

    _, rot31, d31 = mapping[3][1]
    print(rot31, d31)
    o = orient_a_beacon([0, 0, 0], rot31, d31)
    print("3 -> 1: ", o)
    o = orient_a_beacon(o, rot10, d10)
    print("1 -> 0: ", o)

    o = orient_a_beacon([0, 0, 0], rot41, d41)
    print("4 -> 1: ", o)
    o = orient_a_beacon(o, rot10, d10)
    print("1 -> 0: ", o)


def debug_7():
    print("debug 7")
    mapping = pickle.load(open("mapping_debug.pkl", "rb"))

    _, rot42, d42 = mapping[4][2]
    rot24i, d24i = invert(rot42, d42)
    print("42: ", rot42, d42)
    print("24i: ", rot24i, d24i)
    p = orient_a_beacon([0, 0, 0], rot42, d42)
    print("->", p)
    p = orient_a_beacon(p, rot24i, d24i)
    print("->", p)
    print(p)

def debug_8(scanners):
    print(invert_rot((-3, 1, -2)))
    for iscanner1 in [4]:
        beacons1 = scanners[iscanner1]
        for iscanner2 in [1]:
            beacons2 = scanners[iscanner2]
            match, rot, d = compare_scanners(beacons1, beacons2)
            print(f"{iscanner2} -> {iscanner1} = {rot}, {d}")

def compare_scanners(beacons1, beacons2):
    for i, beacon1 in enumerate(beacons1):
        for j, beacon2 in enumerate(beacons2):
            for rot in ROTS:
                d = beacon1 - orient_a_beacon(beacon2, rot)
                beacons2_1 = orient_beacons(beacons2, rot, d)

                match = match_beacons(beacons1, beacons2_1)
                if len(match) >= 12:
                    print(f"  {i} - {j} matched ", len(match), " rot = ", rot, d) 
                    print(match)
                    return match, rot, d
    return [], None, None


def find_transform_path(iscanner, mapping):
    assert iscanner != 0

    def dfs(i, path, mapping):
        path.append(i)
        if 0 in mapping[i]:
            path.append(0)
            return True
        else:
            for j in mapping[i].keys():
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
    #print(scanners[0])
    #debug_1()
    #debug_3(scanners)
    #compare_scanners(scanners[4], scanners[1])
    #compare_scanners(scanners[1], scanners[4])
    #debug_4(scanners)
    #debug_5()
    #debug_6()
    #debug_7()
    #debug_8(scanners)
    #return

    mapping = dict()

    for iscanner1 in range(n_scanners):
        beacons1 = scanners[iscanner1]
        matched = False
        for iscanner2 in range(iscanner1 + 1, n_scanners):
            print(f"comparing scanner {iscanner1} and {iscanner2}")
            beacons2 = scanners[iscanner2]
            match, rot, d = compare_scanners(beacons1, beacons2)
            if len(match) >= 12:
                print("  matched")
                if iscanner2 in mapping:
                    assert iscanner1 not in mapping[iscanner2]
                    mapping[iscanner2][iscanner1] = [match, rot, d]
                else:
                    mapping[iscanner2] = {iscanner1: [match, rot, d]}

                match_inv = np.flip(match, axis=1)
                rot_inv, d_inv = invert(rot, d)
                if iscanner1 in mapping:
                    assert iscanner2 not in mapping[iscanner1]
                    mapping[iscanner1][iscanner2] = [match_inv, rot_inv, d_inv]
                else:
                    mapping[iscanner1] = {iscanner2: [match_inv, rot_inv, d_inv]}

    pickle.dump(mapping, open("mapping.pkl", "wb"))
    #mapping = pickle.load(open("mapping_debug.pkl", "rb"))
    print("mapping ")
    print(mapping)

    paths = {}
    uniques = set()
    for iscanner, beacons in enumerate(scanners):
        if iscanner == 0:
            uniques.update([(b[0], b[1], b[2]) for b in beacons])
            for b in beacons:
                paths[(b[0], b[1], b[2])] = [0]
            continue

        print("iscanner  =", iscanner)
        path = find_transform_path(iscanner, mapping)
        path_orig = list(path)
        i_from = path.pop(0)
        while path:
            i_to = path.pop(0)
            _, rot, d = mapping[i_from][i_to]
            beacons = orient_beacons(beacons, rot, d)
            i_from = i_to

        print(f"scanner {iscanner} has the following duplicates in global coords")
        for b in beacons:
            b = b[0], b[1], b[2]
            if b in uniques:
                print(b)

        uniques.update([(b[0], b[1], b[2]) for b in beacons])

        for b in beacons:
            paths[(b[0], b[1], b[2])] = path_orig

    print("final beacons")
    uniques = list(uniques)
    uniques.sort(key=lambda v: v[0])
    for b in uniques:
        bb = (b[0],b[1],b[2])
        print(f"{b[0]},{b[1]},{b[2]} ({paths[bb]})")
    
    print(f"count = {len(uniques)}")


if __name__ == "__main__":
    main("input.txt")
