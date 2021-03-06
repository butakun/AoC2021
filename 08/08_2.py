import logging

logging.basicConfig(level=logging.DEBUG)

# 0123456
# abcdefg


def do_one(ten, output):

    src2dst = [set()] * 7
    
    done = set()

    # cf
    ten_2 = [v for v in filter(lambda l: len(l) == 2, ten)][0]
    src2dst[2] = set(ten_2)
    src2dst[5] = set(ten_2)
    done = done.union(set(ten_2))
    logging.debug(f"after 2-element codes {ten_2}, done = {done}")
    logging.debug(f"src2dst = {src2dst}")

    # a of acf
    ten_3 = [v for v in filter(lambda l: len(l) == 3, ten)][0]
    src2dst[0] = set(ten_3) - done
    done = done.union(set(ten_3))
    logging.debug(f"after 3-element code {ten_3}, done = {done}")
    logging.debug(f"src2dst = {src2dst}")

    # bd of bcdf
    ten_4 = [v for v in filter(lambda l: len(l) == 4, ten)][0]
    src2dst[1] = set(ten_4) - done
    src2dst[3] = set(ten_4) - done
    done = done.union(set(ten_4))
    logging.debug(f"after 4-element code {ten_4}, done = {done}")
    logging.debug(f"src2dst = {src2dst}")

    # eg of abcdefg
    ten_7 = [v for v in filter(lambda l: len(l) == 7, ten)][0]
    src2dst[4] = set(ten_7) - done
    src2dst[6] = set(ten_7) - done
    done = done.union(set(ten_7))
    logging.debug(f"after 7-element code {ten_7}, done = {done}")
    logging.debug("we now completed the search space")
    logging.debug(f"src2dst = {src2dst}")

    # at this point, the search space is now fixed, the solution is a subset of src2dst.

    # acdeg, acdfg, abdfg
    # adg is common, bcef is not shared.
    ten_5 = [set(v) for v in filter(lambda l: len(l) == 5, ten)]
    logging.debug(f"analyzing 5-element outputs: {ten_5}")
    common = ten_5[0].intersection(ten_5[1]).intersection(ten_5[2])
    src2dst[0] = src2dst[0].intersection(common)
    src2dst[3] = src2dst[3].intersection(common)
    src2dst[6] = src2dst[6].intersection(common)
    logging.debug(f"after 5-element codes, narrowing the space by 3 common elements (adg): {common}")
    logging.debug(f"src2dst = {src2dst}")

    extra = ten_5[0].union(ten_5[1]).union(ten_5[2]) - common
    src2dst[1] = src2dst[1].intersection(extra)
    src2dst[2] = src2dst[2].intersection(extra)
    src2dst[4] = src2dst[4].intersection(extra)
    src2dst[5] = src2dst[5].intersection(extra)
    logging.debug(f"after 5-element codes, narrowing the space by 3 unshared elements (bcef): {extra}")
    logging.debug(f"src2dst = {src2dst}")

    # abcefg, abdefg, abcdfg
    # abfg is common, cde is not shared
    ten_6 = [set(v) for v in filter(lambda l: len(l) == 6, ten)]
    logging.debug(f"analyzing 6-element outputs: {ten_6}")
    common = set.intersection(*ten_6)
    src2dst[0] = src2dst[0].intersection(common)
    src2dst[1] = src2dst[1].intersection(common)
    src2dst[5] = src2dst[5].intersection(common)
    src2dst[6] = src2dst[6].intersection(common)
    logging.debug(f"after 6-element codes, narrowing the space by 4 common elements (abfg): {common}")
    logging.debug(f"src2dst = {src2dst}")

    extra = set.union(*ten_6) - common
    src2dst[2] = src2dst[2].intersection(extra)
    src2dst[3] = src2dst[3].intersection(extra)
    src2dst[4] = src2dst[4].intersection(extra)
    logging.debug(f"after 6-element codes, narrowing the space by 3 unshared elements (cde): {extra}")
    logging.debug(f"src2dst = {src2dst}")
    logging.debug("we now completed the mapping")
    for d in src2dst:
        assert len(d) == 1

    # we build a map now.
    src2dst = [list(d)[0] for d in src2dst]
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
