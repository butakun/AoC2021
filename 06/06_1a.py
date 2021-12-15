import numpy as np
from numpy.linalg import matrix_power


def main(filename):
    lines = []
    with open(filename) as f:
        line = f.readline().strip()
        school = [int(d) for d in line.split(",")]

    x = np.zeros(9, dtype=np.uint64)
    for age in school:
        x[age] += 1
    print(x)

    A = np.array(
            [[0, 1, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0]],
            dtype=np.uint64
                )

    generations = 256
    AA = matrix_power(A, generations)
    x = np.matmul(AA, x)
    print(x, x.sum())


if __name__ == "__main__":
    main("input.txt")
