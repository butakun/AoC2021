import numpy as np
import pickle


def grow_edges(image, edge_bit=0):
    i, j = image.shape
    if edge_bit == 0:
        bigger = np.zeros((i + 2, j + 2), dtype=image.dtype)
    else:
        bigger = np.ones((i + 2, j + 2), dtype=image.dtype)
    bigger[1:-1, 1:-1] = image
    return bigger


def step(image, algo):
    """ image is always surrounded by one-pixel edges at input """

    zeros_algo = algo[0]
    ones_algo = algo[511]  # 111111111
    edge_algo = [zeros_algo, ones_algo]
    print("edge algo = ", edge_algo)

    edge_bit = image[0, 0]

    image = grow_edges(image, edge_bit)
    out = np.zeros_like(image)

    idim, jdim = out.shape
    for i in range(1, idim - 1):
        for j in range(1, jdim - 1):
            pat = image[i-1:i+2,j-1:j+2].flatten()
            pat = "".join(map(str, pat))
            algo_index = int(pat, 2)
            bit = algo[algo_index]
            out[i, j] = bit

    for i in range(idim):
        out[i,      0] = edge_algo[image[i,      0]]
        out[i, jdim-1] = edge_algo[image[i, jdim-1]]
    for j in range(jdim):
        out[     0, j] = edge_algo[image[     0, j]]
        out[idim-1, j] = edge_algo[image[idim-1, j]]

    return out


def pretty(image):
    buf = ""
    for l in image:
        buf += "".join(map(str, l)).replace("0", ".").replace("1", "#") + "\n"
    return buf.strip()


def main(filename):
    with open(filename) as f:
        line = f.readline().strip()
        assert len(line) == 512
        algo = line.replace("#", "1").replace(".", "0")
        algo = np.array(list(map(int, list(algo))))
        f.readline()

        image = []
        for line in f:
            bits = line.strip().replace("#", "1").replace(".", "0")
            bits = list(map(int, bits))
            image.append(bits)
        image = np.array(image)

    print(algo)
    image = grow_edges(image)
    print(pretty(image))

    out = step(image, algo)
    print(pretty(out))
    print("# of pixels lit = ", out.sum())
    out = step(out, algo)
    print(pretty(out))
    print("# of pixels lit = ", out.sum())


if __name__ == "__main__":
    main("input.txt")
