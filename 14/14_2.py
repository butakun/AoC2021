import numpy as np


def find_all(template, pair):
    found = []
    i0 = 0
    while True:
        try:
            i = template[i0:].index(pair)
            found.append(i0 + i)
            i0 += i + 1
        except ValueError:
            break
    return found


def insert(template, inserts):
    elements = list(template)
    for i, element in inserts:
        elements.insert(i, element)
        #print(f"{element} inserted at {i}: {''.join(elements)}")

    return "".join(elements)


def step_(template, rules):
    inserts = []
    for pair, element in rules:
        ii0 = find_all(template, pair)
        for i in ii0:
            inserts.append([i + 1, element])

    inserts.sort(key=lambda a: a[0])
    #print(inserts)

    for inc in range(len(inserts)):
        inserts[inc][0] += inc
    #print(inserts)

    template = insert(template, inserts)
    return template


def step(pairs, rules):
    for pair, element in rules.items():
        new_pair1 = pair[0] + element
        new_pair2 = element + pair[1]
        print("rule ", pair, " -> ", element, " new pairs ", new_pair1, new_pair2)

        ii0 = pairs[pair]
        if len(ii0) > 0:
            print(" exists at ", ii0)
        inserts = {}
        if new_pair1 in rules:
            inserts[new_pair1] = list(ii0)
        if new_pair2 in rules:
            inserts[new_pair2] = [i+1 for i in ii0]

        print(inserts)


def frequency(template):
    freq = {}
    for element in set(template):
        occur = len(template) - len(template.replace(element, ""))
        freq[element] = occur
    return freq

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

    pairs = {}
    for pair, element in rules.items():
        ii = find_all(template, pair)
        assert pair not in pairs
        pairs[pair] = ii
    print(pairs)

    for i in range(1):
        step(pairs, rules)
    return

    print(template, len(template))
    freq = frequency(template)
    print(freq)

    ff = np.array([v for k, v in freq.items()])
    print(ff.max(), ff.min(), ff.max() - ff.min())


if __name__ == "__main__":
    main("input_debug.txt")
