import numpy as np
import pickle


def mark_a_number(board, num):
    print(board)
    board[:, :, 1][board[:, :, 0] == num] = 1


def is_done(board):
    rows = np.zeros(5, np.int32)
    cols = np.zeros(5, np.int32)
    for i in range(5):
        if np.all(board[i, :, 1] == 1):
            rows[i] = 1
    for i in range(5):
        if np.all(board[:, i, 1] == 1):
            cols[i] = 1

    done = rows.sum() > 0 or cols.sum() > 0
    return done


def get_score(board, last_num):
    unmarked = np.sum(board[:, :, 0][board[:, :, 1] == 0])
    return unmarked * last_num


def main(filename):
    with open(filename) as f:
        line = f.readline().strip()
        drawn_nums = [int(i) for i in line.split(",")]

        iboard = 0
        irow = 0
        boards = []
        board = []
        for line in f:
            if irow > 0:
                board.append([int(i) for i in line.strip().split()])
            irow += 1
            if irow > 5:
                boards.append(board)
                board = []
                irow = 0

    boards= np.array(boards)
    num_boards = boards.shape[0]
    boards2 = np.zeros((num_boards, 5, 5, 2), np.int32)
    boards2[:, :, :, 0] = boards

    #np.save(open("boards.npy", "wb"), boards2)

    boards = boards2

    done = []
    for iturn, num in enumerate(drawn_nums):
        for iboard in range(num_boards):
            mark_a_number(boards[iboard], num)

        print(f"Turn {iturn}")
        for iboard in range(num_boards):
            board = boards[iboard, :, :, :]
            if is_done(board):
                done.append(iboard)
                print(f"Board {iboard} is done")
                print(board[:, :, 0])
                print(board[:, :, 1])
                score = get_score(board, num)
                print(f"score = {score}")
                break

        if len(done) > 0:
            break


if __name__ == "__main__":
    main("input.txt")
