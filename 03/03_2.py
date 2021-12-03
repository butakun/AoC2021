import numpy as np
import pickle


def main(filename):
    with open(filename) as f:
        report = [line.strip() for line in f]

    report = np.array([[int(i) for i in l] for l in report])
    np.save(open("report.npy", "wb"), report)

    print(report)

    N, M = report.shape
    o2 = report
    co2 = report
    o2_final, co2_final = None, None
    for j in range(M):
        ones = o2[:, j].sum()
        zeros = o2.shape[0] - ones
        most_common = 1 if ones >= zeros else 0
        least_common = 1 if ones < zeros else 0
        print(j, ones, zeros, most_common, least_common)
        o2 = o2[o2[:, j] == most_common]
        print(o2)
        if o2_final is None and o2.shape[0] == 1:
            o2_final = o2[0]
            break

    print(o2_final)

    for j in range(M):
        ones = co2[:, j].sum()
        zeros = co2.shape[0] - ones
        most_common = 1 if ones >= zeros else 0
        least_common = 1 if ones < zeros else 0
        print(j, ones, zeros, most_common, least_common)
        co2 = co2[co2[:, j] == least_common]
        print(co2)
        if co2_final is None and co2.shape[0] == 1:
            co2_final = co2[0]
            break

    print(co2_final)
    print("final ", o2_final, co2_final)

    o2_final = "".join(map(str, o2_final.tolist()))
    co2_final = "".join(map(str, co2_final.tolist()))
    print(o2_final, co2_final)

    o2_final = int(o2_final, 2)
    co2_final = int(co2_final, 2)
    print(o2_final, co2_final, o2_final * co2_final)


if __name__ == "__main__":
    main("input.txt")
