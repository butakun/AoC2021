import numpy as np
import itertools


# 0123456
# abcdefg

def do_one(ten, output):

    src2dst = [set()] * 7

    # cf
    ten_2 = [v for v in filter(lambda l: len(l) == 2, ten)][0]
    print(ten_2)
    src2dst[2] = set(ten_2)
    src2dst[5] = set(ten_2)
    done = set(ten_2)

    # acf
    ten_3 = [v for v in filter(lambda l: len(l) == 3, ten)][0]
    print(ten_3)
    i3 = set(ten_3) - set(ten_2)
    c3 = i3.pop()
    i3 = ord(c3) - ord("a")
    src2dst[0] = set([c3])
    done.add(c3)

    print(src2dst)

    # bd of bcdf
    ten_4 = [v for v in filter(lambda l: len(l) == 4, ten)][0]
    print(ten_4)
    src2dst[1] = set(ten_4) - done
    src2dst[3] = set(ten_4) - done
    done = done.union(set(ten_4))
    print("src2dst = ", src2dst)

    # eg of abcdefg
    ten_7 = [v for v in filter(lambda l: len(l) == 7, ten)][0]
    print(ten_7, set(ten_7) - done)
    src2dst[4] = set(ten_7) - done
    src2dst[6] = set(ten_7) - done
    print("src2dst = ", src2dst)

    # acdeg, acdfg, abdfg
    # adg is common
    ten_5 = [set(v) for v in filter(lambda l: len(l) == 5, ten)]
    print(ten_5)
    common = ten_5[0].intersection(ten_5[1]).intersection(ten_5[2])
    print(common)
    src2dst[0] = src2dst[0].intersection(common)
    src2dst[3] = src2dst[3].intersection(common)
    src2dst[6] = src2dst[6].intersection(common)
    print("src2dst = ", src2dst)

    # abcefg, abdefg, abcdfg
    # abfg is common
    ten_6 = [set(v) for v in filter(lambda l: len(l) == 6, ten)]
    print(ten_6)
    common = ten_6[0].intersection(ten_6[1]).intersection(ten_6[2])
    print(common)
    src2dst[0] = src2dst[0].intersection(common)
    src2dst[1] = src2dst[1].intersection(common)
    src2dst[5] = src2dst[5].intersection(common)
    src2dst[6] = src2dst[6].intersection(common)
    print("src2dst = ", src2dst)

    fixed = set([list(f)[0] for f in src2dst if len(f) == 1])
    print("fixed = ", fixed)
    for i, d in enumerate(src2dst):
        if len(d) > 1:
            src2dst[i] = d.difference(fixed)
    print("src2dst = ", src2dst)

    src2dst = [list(d)[0] for d in src2dst]
    print("src2dst = ", src2dst)
    src = "abcdefg"
    src2dst_map = {}
    for i, d in enumerate(src2dst):
        src2dst_map[chr(i + ord("a"))] = d
    print("src2dst_map = ", src2dst_map)

    digits_orig = ["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]
    mess2digit = {}
    for i, orig in enumerate(digits_orig):
        mess = [src2dst_map[s] for s in orig]
        mess_key = "".join(sorted(mess))
        mess2digit[mess_key] = i
    print("mess2digit = ", mess2digit)

    output_orig = []
    for mess in output:
        mess_key = "".join(sorted(mess))
        output_orig.append(mess2digit[mess_key])
    output_orig_num = int("".join(map(str, output_orig)))
    print(output_orig,output_orig_num)
    return output_orig_num


def main(filename):
    with open(filename) as f:
        tens = []
        outputs = []
        for line in f:
            ten, output = line.strip().split("|")
            output = [o for o in output.strip().split()]
            ten = [t for t in ten.strip().split()]
            tens.append(ten)
            outputs.append(output)

    acc = 0
    for ten, output in zip(tens, outputs):
        acc += do_one(ten, output)
    print(acc)

if __name__ == "__main__":
    main("input.txt")
