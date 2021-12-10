import numpy as np


def score(c):
    if c == ")":
        return 1
    elif c == "]":
        return 2
    elif c == "}":
        return 3
    elif c == ">":
        return 4
    else:
        raise ValueError(c)


def do_line(line):
    stack = []
    corrupt = False
    incomplete = False
    for i, c in enumerate(line):
        if c in "([{<":
            stack.append(c)
        elif c in ")]}>":
            c_open = stack.pop()
            pair = c_open + c
            if pair != "()" and pair != "[]" and pair != "{}" and pair != "<>":
                corrupt = True
                return 0
    if len(stack) == 0:
        return 0

    score_total = 0
    add = ""
    for c_open in reversed(stack):
        if c_open == "(":
            c_close = ")"
        elif c_open == "[":
            c_close = "]"
        elif c_open == "{":
            c_close = "}"
        elif c_open == "<":
            c_close = ">"
        else:
            raise ValueError(c_open)
        add += c_close
        score_total = score_total * 5 + score(c_close)

    print("incomplete", stack, add, score_total)

    return score_total


def main(filename):
    with open(filename) as f:
        lines = [l.strip() for l in f]

    scores = []
    for i, line in enumerate(lines):
        s = do_line(line)
        if s > 0:
            scores.append(s)

    scores2 = sorted(scores)
    print(scores2)

    score = scores2[len(scores2) // 2]
    print(score)

if __name__ == "__main__":
    main("input.txt")
