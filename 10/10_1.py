import numpy as np


def score(c):
    if c == ")":
        return 3
    elif c == "]":
        return 57
    elif c == "}":
        return 1197
    elif c == ">":
        return 25137
    else:
        raise ValueError(c)


def do_line(line):
    stack = []
    corrupt = False
    for i, c in enumerate(line):
        if c in "([{<":
            stack.append(c)
        elif c in ")]}>":
            c_open = stack.pop()
            pair = c_open + c
            if pair != "()" and pair != "[]" and pair != "{}" and pair != "<>":
                corrupt = True
                sc = score(c)
                print(pair, sc)
                return sc
    if len(stack) > 0:
        print("incomplete")
    return 0


def main(filename):
    with open(filename) as f:
        lines = [l.strip() for l in f]

    acc = 0
    for i, line in enumerate(lines):
        acc += do_line(line)

    print(acc)

if __name__ == "__main__":
    main("input.txt")
