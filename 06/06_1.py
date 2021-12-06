import numpy as np


def main(filename):
    lines = []
    with open(filename) as f:
        line = f.readline().strip()
        school = [int(d) for d in line.split(",")]

    np.save(open("school.npy", "wb"), school)
    print(school)

    NDAYS = 80
    for day in range(1, NDAYS + 1):
        babies = []
        for i, fish in enumerate(school):
            if fish > 0:
                school[i] -= 1
            elif fish == 0:
                school[i] = 6
                babies.append(8)
        school.extend(babies)
        print(day, len(school))
        #print(day, len(school), school)


if __name__ == "__main__":
    main("input.txt")
