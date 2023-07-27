import json


def print_board(board):
    for i in range(9):
        for j in range(9):
            print(board.getItem(i, j), end=" ")
            if (j + 1) % 3 == 0:
                print("|", end=" ")
        print()
        if (i + 1) % 3 == 0:
            print("- " * 11)


class SolveData:
    def __init__(self, board) -> None:
        self.data = {}
        self.board = board

    def store(self, step):
        self.data[step] = self.board.get_current_state()

    def save(self, filename):
        with open(filename, "w+") as f:
            json.dump(self.data, f)
