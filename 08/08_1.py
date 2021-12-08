import numpy as np


def main(filename):
    with open(filename) as f:
        outputs = []
        for line in f:
            ten, output = line.strip().split("|")
            output = [o for o in output.strip().split()]
            outputs.append(output)

    ones, fours, sevens, eights = 0, 0, 0, 0
    for output in outputs:
        for o in output:
            l = len(o)
            if l == 2:
                ones += 1
            elif l == 4:
                fours += 1
            elif l == 3:
                sevens += 1
            elif l == 7:
                eights += 1
            print(output, l, ones, fours, sevens, eights)

    print(ones + fours + sevens + eights)


if __name__ == "__main__":
    main("input.txt")
