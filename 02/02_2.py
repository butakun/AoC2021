import numpy as np


def main(filename):
    with open(filename) as f:
        commands = [line.split() for line in f]
        commands = [(l[0], int(l[1])) for l in commands]

    def command_delta(command, i):
        if command == "forward":
            return [i, 0]
        elif command == "up":
            return [0, -i]
        elif command == "down":
            return [0, i]

    commands = np.array([command_delta(*command) for command in commands])

    xya = np.zeros((commands.shape[0], 3), np.int32)
    xya[:, 0] = commands[:, 0].cumsum()
    xya[:, 2] = commands[:, 1].cumsum()
    xya[:, 1] = (commands[:, 0] * xya[:, 2]).cumsum()
    print(xya[-1, :])
    print(xya[-1, 0] * xya[-1, 1])


if __name__ == "__main__":
    main("input.txt")
