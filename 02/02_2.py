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

    x, y, aim = 0, 0, 0
    for command in commands:
        x += command[0]
        y += command[0] * aim
        aim += command[1]
        print(x, y, aim)

    print(x * y)


if __name__ == "__main__":
    main("input.txt")
