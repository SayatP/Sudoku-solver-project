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


class SolveDataStore:
    def __init__(self, board) -> None:
        self.data = {}
        self.board = board
        self.index = 0

    def store(self, step, domains):
        self.data[self.index] = {'board': self.board.get_current_state(), 'step': step}

        if domains is not None:
            self.data['domains'] = {f"{k[0]}{k[1]}": list(v) for k,v in domains.items()}
        self.index += 1
    
    def save(self, filename):
        with open(filename, "w+") as f:
            json.dump(self.data, f)
