import numpy as np
from functools import reduce


class Pairs:
    def __init__(self):
        self.first = None
        self.pairs = {}


def step(pairs, first_pair, rules):
    first_pair_new = None
    pairs_new = {}

    pair = first_pair
    next_pair, next_pair_index = pairs[pair][0]
    first_pair_new = None
    while pair != None:

        element = rules[pair]
        pair_new_1 = pair[0] + element
        pair_new_2 = element + pair[1]

        if first_pair_new is None:
            first_pair_new = pair_new_1

        if pair_new_2 in pairs_new:
            pair_new_2_index = len(pairs_new[pair_new_2])
        else:
            pair_new_2_index = 0

        if pair_new_1 in pairs_new:
            pairs_new[pair_new_1].append((pair_new_2, pair_new_2_index))
        else:
            if pair_new_1 == pair_new_2:
                pairs_new[pair_new_1] = [(pair_new_2, 1)]
            else:
                pairs_new[pair_new_1] = [(pair_new_2, pair_new_2_index)]

        if next_pair is None:
            next_pair_new = None
            next_pair_new_index = 0
        else:
            c2 = rules[next_pair]
            next_pair_new = pair[1] + c2
            if next_pair_new in pairs_new:
                next_pair_new_index = len(pairs_new[next_pair_new])
            else:
                next_pair_new_index = 0

        #print(f"{pair} -> {next_pair},{next_pair_index} => {pair_new_1} x {pair_new_2} => {next_pair_new},{next_pair_new_index}")

        if pair_new_2 in pairs_new:
            pairs_new[pair_new_2].append((next_pair_new, next_pair_new_index))
        else:
            if pair_new_2 == next_pair_new:
                pairs_new[pair_new_2] = [(next_pair_new, 1)]
            else:
                pairs_new[pair_new_2] = [(next_pair_new, next_pair_new_index)]

        pair = next_pair
        if pair is not None:
            next_pair, next_pair_index = pairs[next_pair][next_pair_index]

    return pairs_new, first_pair_new


def frequency(pairs, first_pair):
    counts = {}
    pair = first_pair
    pair_index = 0
    counts[pair[0]] = 1
    counts[pair[1]] = 0
    while pair is not None:
        if pair[1] in counts:
            counts[pair[1]] += 1
        else:
            counts[pair[1]] = 1
        pair, pair_index = pairs[pair][pair_index]

    return counts


def main(filename):
    with open(filename) as f:
        template = f.readline().strip()
        f.readline()
        rules = {}
        for line in f:
            pair, element = line.strip().split(" -> ")
            rules[pair] = element

    print(template)
    print(rules)

    first_pair = None
    pairs = {}
    ps = [template[i] + template[i + 1] for i in range(len(template) - 1)]
    print(ps)

    first_pair = ps[0]
    num_ps = len(ps)
    for i, pair in enumerate(ps):
        next_pair = None
        if i < num_ps - 1:
            next_pair = ps[i + 1]
            next_pairs = pairs.get(next_pair, [])
            next_pair_index = len(next_pairs)

        if pair in pairs:
            pairs[pair].append((next_pair, next_pair_index))
        else:
            pairs[pair] = [(next_pair, 0)]

    print(pairs, first_pair)

    for i in range(10):
        pairs, first_pair = step(pairs, first_pair, rules)
        print(i)
        print(pairs, first_pair)

    freq = frequency(pairs, first_pair)
    print(freq)

    freqs = np.array([v for k, v in freq.items()])
    print(freqs.max(), freqs.min(), freqs.max() - freqs.min())

if __name__ == "__main__":
    main("input_debug.txt")
