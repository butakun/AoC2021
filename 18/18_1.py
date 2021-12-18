import numpy as np


def parse_pair(buf):
    print(f"parsing {buf}")
    assert(buf[0] == "[" and buf[-1] == "]")
    if buf[1] == "[":
        left, icomma = parse_pair(buf[1:])
        icomma += 1  # it was relative to buf[1:]
    else:
        icomma = buf.find(",")
        left = int(buf[1:icomma])

    if buf[icomma + 1] == "[":
        right, iclose = parse_pair(buf[icomma+1:])
        iclose += icomma + 1 + 1
    else:
        iclose = buf[icomma+1:].find("]")
        right = int(buf[icomma+1:icomma+1+iclose])
        iclose = icomma + 1 + iclose + 1

    print("  found ", left, right, iclose)
    return [left, right], iclose


def parse_flat(buf):
    flat = []
    i = 0
    while i < len(buf):
        if buf[i] in ["[", "]", ","]:
            flat.append(buf[i])
            i += 1
        else:
            i2 = len(buf[i:])
            i2_ = buf[i:].find("[")
            if i2_ >= 0:
                i2 = min(i2, i2_)
            i2_ = buf[i:].find("]")
            if i2_ >= 0:
                i2 = min(i2, i2_)
            i2_ = buf[i:].find(",")
            if i2_ >= 0:
                i2 = min(i2, i2_)
            val = int(buf[i:i+i2])
            flat.append(val)
            i = i + i2
    return flat


def reduce(flat):
    depth = 0
    action = None
    iaction = None
    # explode?
    for i, node in enumerate(flat):
        if node == "[":
            depth += 1
        elif node == "]":
            depth -= 1
        elif node == ",":
            pass
        elif depth > 4:
            assert flat[i + 1] == ","
            if isinstance(flat[i + 2], int):
                action = "explode"
                iaction = i
                break

    if action is None:
        for i, node in enumerate(flat):
            if isinstance(flat[i], int):
                if node >= 10:
                    action = "split"
                    iaction = i
                    break

    if action is None:
        return False, flat

    if action == "explode":
        print("exploding at ", iaction, ": ", flat[iaction], flat[iaction + 2])
        ileft = iaction - 1
        while ileft > 0:
            if isinstance(flat[ileft], int):
                break
            ileft -= 1
        if ileft > 0:
            print(" left value at ", ileft, " = ", flat[ileft])
            flat[ileft] += flat[iaction]
        iright = iaction + 3
        while iright < len(flat):
            if isinstance(flat[iright], int):
                break
            iright += 1
        if iright < len(flat):
            print(" right value at ", iright, " = ", flat[iright])
            flat[iright] += flat[iaction + 2]

        flat_ = flat[:iaction-1]
        flat_.append(0)
        flat_.extend(flat[iaction+4:])
        flat = flat_
        return True, flat

    if action == "split":
        v = flat[iaction]
        print("splitting at ", iaction, ": ", v)
        left = v // 2
        right = left + v % left
        flat[iaction] = "["
        flat.insert(iaction + 1, left)
        flat.insert(iaction + 2, ",")
        flat.insert(iaction + 3, right)
        flat.insert(iaction + 4, "]")
        return True, flat


def main(filename):
    with open(filename) as f:
        flats = [parse_flat(line.strip()) for line in f]

    # reduction
    flat = flats.pop(0)
    while flats:
        flat2 = flats.pop(0)
        flat.append(",")
        flat.extend(flat2)
        flat.insert(0, "[")
        flat.append("]")

        print("processing: ", "".join(map(str, flat)))
        reduced = True
        while reduced:
            reduced, flat = reduce(flat)
            print("-> ", "".join(map(str, flat)))

    # move to tree
    tree = eval("".join(map(str, flat)))
    print(tree)

    def magnitude(node):
        if isinstance(node, int):
            return node
        else:
            return 3 * magnitude(node[0]) + 2 * magnitude(node[1])

    print(magnitude(tree))


if __name__ == "__main__":
    main("input.txt")
