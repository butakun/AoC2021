import numpy as np
import pickle


def main(filename):
    with open(filename) as f:
        report = [line.strip() for line in f]

    report = np.array([[int(i) for i in l] for l in report])
    #np.save(open("report.npy", "wb"), report)

    N, M = report.shape
    o2 = report
    co2 = report
    o2_final, co2_final = None, None

    for j in range(M):
        ones = o2[:, j].sum()
        zeros = o2.shape[0] - ones
        most_common = 1 if ones >= zeros else 0
        o2 = o2[o2[:, j] == most_common]
        if o2.shape[0] == 1:
            break

    o2 = o2[0]
    o2 = "".join([str(i) for i in o2.tolist()])
    o2 = int(o2, 2)
    print(f"O2 = {o2}")

    for j in range(M):
        ones = co2[:, j].sum()
        zeros = co2.shape[0] - ones
        least_common = 1 if ones < zeros else 0
        co2 = co2[co2[:, j] == least_common]
        if co2.shape[0] == 1:
            break

    co2 = co2[0]
    co2 = "".join([str(i) for i in co2.tolist()])
    co2 = int(co2, 2)
    print(f"CO2 = {co2}")

    print(f"O2 * CO2 = {o2 * co2}")


if __name__ == "__main__":
    main("input.txt")
