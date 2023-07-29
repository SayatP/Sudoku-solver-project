import json
from copy import deepcopy
from os import path


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
        self.data[self.index] = {
            "board": deepcopy(self.board.get_current_state()),
            "step": step,
        }

        domain = deepcopy({f"{k[0]}{k[1]}": list(v) for k, v in domains.items()})
        domain = self.convert_domain(domain)
        self.data[self.index]["domains"] = domain
        self.index += 1

    def save(self, filename):
        final_data = {}
        for value in self.data.values():
            final_data[value["step"]] = value

        file_path = path.abspath(filename)
        with open(file_path, "w") as f:
            json.dump(final_data, f)

    def save_board(self, board, filename):
        final_data = {}
        final_data[1] = {"board": board, "step": 1, "domains": []}
        file_path = path.abspath(filename)
        with open(file_path, "w") as f:
            json.dump(final_data, f)

    def convert_domain(self, domain):
        base = [[[] for _ in range(9)] for _ in range(9)]

        for k, value in domain.items():
            if self.board.data[int(k[0])][int(k[1])] == 0:
                base[int(k[0])][int(k[1])] = value

        return base
