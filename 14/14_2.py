import numpy as np
from functools import reduce


def frequency(frequencies, first_pair, last_pair):
    counts = {}
    none_zero_indices = np.where(frequencies > 0)[0]
    for i in none_zero_indices:
        count = frequencies[i]
        pair = pair_from_index(i)
        c1 = pair[0]
        if c1 not in counts:
            counts[c1] = count
        else:
            counts[c1] += count

    last_char = last_pair[1]
    if last_char not in counts:
        counts[last_char] = 1
    else:
        counts[last_char] = counts[last_char] + 1

    return counts


def index_from_pair(pair):
    i1 = ord(pair[0]) - 65
    i2 = ord(pair[1]) - 65
    return i1 * 26 + i2


def pair_from_index(index):
    i1 = index // 26
    i2 = index % 26
    return chr(i1 + 65) + chr(i2 + 65)


def dump_pairs(frequencies, first_pair, last_pair):
    none_zero_indices = np.where(frequencies > 0)[0]
    print(none_zero_indices)
    for i in none_zero_indices:
        pair = pair_from_index(i)
        count = frequencies[i]
        print(f"{pair}: {count}")
    print(f"  first = {first_pair}, last = {last_pair}")


def step(frequencies, frequencies_next, first_pair, last_pair,  rules):
    element = rules[first_pair]
    first_pair_next = first_pair[0] + element
    element = rules[last_pair]
    last_pair_next = element + last_pair[1]

    for pair, element in rules.items():
        index = index_from_pair(pair)
        count = frequencies[index]
        pair_new_1 = pair[0] + element
        pair_new_2 = element + pair[1]
        index_new_1 = index_from_pair(pair_new_1)
        index_new_2 = index_from_pair(pair_new_2)
        frequencies_next[index_new_1] += count
        frequencies_next[index_new_2] += count

    return first_pair_next, last_pair_next


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
    N = 26 * 26

    frequencies = np.zeros(N, dtype=np.uint64)

    first_pair, last_pair = None, None
    for i in range(len(template) - 1):
        pair = template[i:i+2]
        pair_index = index_from_pair(pair)
        frequencies[pair_index] += 1
        if first_pair is None:
            first_pair = pair
        last_pair = pair

    dump_pairs(frequencies, first_pair, last_pair)

    frequencies_next = np.zeros_like(frequencies, dtype=np.uint64)

    for i in range(40):
        first_pair_next, last_pair_next = step(frequencies, frequencies_next, first_pair, last_pair,  rules)
        print("step ", i)
        dump_pairs(frequencies_next, first_pair_next, last_pair_next)

        tmp = frequencies
        frequencies = frequencies_next
        frequencies_next = tmp
        frequencies_next[:] = 0
        first_pair, last_pair = first_pair_next, last_pair_next

        print(frequency(frequencies, first_pair, last_pair))

    freq = frequency(frequencies, first_pair, last_pair)
    print(freq)

    freqs = np.array([v for k, v in freq.items()], dtype=np.uint64)
    print(freqs.max(), freqs.min(), freqs.max() - freqs.min())

if __name__ == "__main__":
    main("input.txt")
