import numpy as np
import pickle


def get_coords_on_axis(beacons, axis):
    beacons_ = beacons[:, abs(axis) - 1]
    if axis < 0:
        beacons_ = -beacons_
    return beacons_


def match_1d(values1, values2):
    vmin = min(values1.min(), values2.min())
    vmax = max(values1.max(), values2.max())
    length = vmax - vmin + 1
    grid1 = np.zeros((length), bool)
    grid2 = np.zeros((length), bool)
    grid1[values1 - vmin] = True
    grid2[values2 - vmin] = True
    matched = np.logical_and(grid1, grid2)
    return matched.sum() >= 12


def align_1d(coords1, coords2, first_align=False):
    sorted1 = np.sort(coords1)
    sorted2 = np.sort(coords2)

    min1 = sorted1.min()
    max1 = sorted1.max()

    shifts = []
    for i2 in range(-2000, 2001):
        shifted2 = sorted2 + i2
        overlap2 = np.logical_and(shifted2 >= min1, shifted2 <= max1)
        if np.any(overlap2):
            overlapped2 = shifted2[overlap2]
            min2 = overlapped2.min()
            max2 = overlapped2.max()
            overlap1 = np.logical_and(sorted1 >= min2, sorted1 <= max2)
            if np.any(overlap1):
                overlapped1 = sorted1[overlap1]
                matched = match_1d(overlapped1, overlapped2)
                if matched:
                    shifts.append(i2)
                if first_align:
                    return shifts
        else:
            continue
    return shifts


def compare_scanners(beacons1, beacons2):
    rot = {}
    shift = {}
    for axis1 in [1, 2, 3]:
        coords1 = get_coords_on_axis(beacons1, axis1)
        for axis2 in [1, 2, 3, -1, -2, -3]:
            coords2 = get_coords_on_axis(beacons2, axis2)
            shifts_ = align_1d(coords1, coords2, first_align=True)
            if shifts_:
                assert len(shifts_) == 1
                print(f"Axis {axis1} <-> Axis {axis2}")
                print(shifts_)
                rot[axis1] = axis2
                shift[axis1] = shifts_[0]
                break

    if len(rot) < 3:
        return {}, {}

    return rot, shift


def debug_1():
    overlap = [i * 2 for i in range(12)]
    values1 = [-10, -7, -3]
    values1.extend(overlap)
    for d in [5, 2, 4]:
        values1.append(values1[-1] + d)
    values2 = list(overlap)
    for d in [9, 1, 5]:
        values2.append(values2[-1] + d)

    values1 = np.array(values1)
    values2 = np.array(values2)
    print(values1)
    print(values2)

    matched = match_1d(values1, values2)
    if matched:
        print("overlapped at least 12 times")

    shifts = align_1d(values1, values2)
    print("shifts to the 2nd vector: ", shifts)


def debug_2():
    scanners = read_scanners("input_debug.txt")
    beacons1 = scanners[0]
    beacons2 = scanners[1]
    values1 = beacons1[:, 0]
    values2 = -beacons2[:, 0]
    print(values1)
    print(values2)
    shifts = align_1d(values1, values2)
    print(shifts)


def debug_3():
    scanners = read_scanners("input_debug.txt")
    for i, j in [[0, 1], [1, 3], [1, 4], [2, 4]]:
        print(f"comparing scanners {i} and {j}")
        rot, shift = compare_scanners(scanners[i], scanners[j])
        print(f"  rot: {rot}, shift: {shift}")


def debug_4():
    scanners = read_scanners("input_debug.txt")
    beacons1 = scanners[2]
    beacons2 = scanners[4]
    values1 = beacons1[:, 0]
    values2 = beacons2[:, 1]
    shifts = align_1d(values1, values2)
    values1 = np.sort(values1)
    values2 = np.sort(values2)
    print(f"values1: {values1}")
    print(f"values2: {values2}")
    print(f"shifts: {shifts}")

    values1 = -beacons1[:, 0]
    values2 = -beacons2[:, 1]
    shifts = align_1d(values1, values2)
    values1 = np.sort(values1)
    values2 = np.sort(values2)
    print(f"values1: {values1}")
    print(f"values2: {values2}")
    print(f"shifted2: {values2 + shifts[0]}")
    print(f"shifts: {shifts}")


def read_scanners(filename):
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
    return scanners


def main(filename):
    scanners = read_scanners(filename)
    n_scanners = len(scanners)

    if False:
        mapping = {}
        for i in range(n_scanners):
            for j in range(i+1, n_scanners):
                print(f"comparing scanners {i} and {j}")
                rot, shift = compare_scanners(scanners[i], scanners[j])
                if len(rot) > 0:
                    print(f"  rot: {rot}, shift: {shift}")
                    if i in mapping:
                        mapping[i][j] = {"rot": rot, "shift": shift}
                    else:
                        mapping[i] = {j: {"rot": rot, "shift": shift}}

        pickle.dump(mapping, open("mapping_b.pkl", "wb"))
    else:
        mapping = pickle.load(open("mapping_b.pkl", "rb"))



if __name__ == "__main__":
    main("input.txt")
