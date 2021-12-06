import numpy as np


def main(filename):
    lines = []
    with open(filename) as f:
        line = f.readline().strip()
        school = [int(d) for d in line.split(",")]

    #np.save(open("school.npy", "wb"), school)
    print(school)

    pop = np.zeros(9, np.int64)
    for age in school:
        pop[age] += 1
    print(0, pop.sum(), pop)

    NDAYS = 256
    for day in range(1, NDAYS + 1):
        pop_next = np.zeros(9, np.int64)
        pop_next[:8] = pop[1:]
        pop_next[6] += pop[0]
        pop_next[8] = pop[0]

        print(day, pop_next.sum(), pop_next)
        pop = pop_next


if __name__ == "__main__":
    main("input.txt")
