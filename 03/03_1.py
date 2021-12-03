import numpy as np
import pickle


def main(filename):
    with open(filename) as f:
        report = [line.strip() for line in f]

    #def split_digits(d):
    #    return np.array([int(i) for i in d])
    #pickle.dump(report, open("report.pkl", "wb"))

    report = np.array([[int(i) for i in l] for l in report])

    print(report)

    N, M = report.shape
    gamma = ""
    epsilon = ""
    for j in range(M):
        ones = report[:, j].sum()
        zeros = N - ones
        most_common = 1 if ones > zeros else 0
        least_common = 1 if ones < zeros else 0
        print(j, ones, zeros, most_common, least_common)
        gamma += f"{most_common}"
        epsilon += f"{least_common}"

    print(gamma, epsilon)
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    print(gamma, epsilon, gamma * epsilon)


if __name__ == "__main__":
    main("input.txt")
