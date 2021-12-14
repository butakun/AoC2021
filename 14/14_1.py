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


def step(template, rules):
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
        rules = []
        for line in f:
            pair, element = line.strip().split(" -> ")
            rules.append([pair, element])

    print(template)
    print(rules)
    for i in range(10):
        template = step(template, rules)

    print(template, len(template))
    freq = frequency(template)
    print(freq)

    ff = np.array([v for k, v in freq.items()])
    print(ff.max(), ff.min(), ff.max() - ff.min())


if __name__ == "__main__":
    main("input.txt")
