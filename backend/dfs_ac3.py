from queue import Queue
from copy import copy

from choose_empty_cell import find_empty_cell

from shared.board import Board
from shared.validation import get_basic_domain

from shared.output import print_board, SolveData

global STEP
STEP = 0


def ac3(board):
    queue = Queue()
    domains = {}
    # set base domains
    for row in range(9):
        for col in range(9):
            domain = get_basic_domain(board, row, col)
            domains[(row, col)] = set(domain)

    [queue.put((i, j)) for i in range(9) for j in range(9) if board.getItem(i, j) == 0]

    while queue:
        i, j = queue.get()
        cell_value = board.getItem(i, j)

        for ni, nj in board.get_neighbors(i, j):
            if board.getItem(ni, nj) == 0:
                new_domain = domains[(ni, nj)].difference({cell_value})

                if domains[(ni, nj)] != new_domain:
                    domains[(ni, nj)] = new_domain
                    queue.append((ni, nj))

    return domains


def solve_sudoku(board: Board, data_store):
    global STEP
    data_store.store(STEP)

    empty_cell = find_empty_cell(board)

    if not empty_cell:
        return True  # The board is already filled, so it's solved

    row, col = empty_cell
    domain = ac3(board)
    set_at_lest_one_by_ac3 = False

    for cell, values in domain.items():
        if len(values) == 1:
            row, col = cell
            board.setItem(row, col, next(iter(values)))

    if set_at_lest_one_by_ac3:
        STEP += 1
        if solve_sudoku(board, data_store):
            return True

    else:
        for cell, values in domain.items():
            i, j = cell
            for value in values:
                board.setItem(row, col, value)
                STEP += 1
                if solve_sudoku(board, data_store):
                    return True

                board.setItem(row, col, 0)

    return False


# Example Sudoku board (0 represents empty cells)
input_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


if __name__ == "__main__":
    board = Board(input_board)
    data_store = SolveData(board)
    if solve_sudoku(board, data_store):
        print("Sudoku solved:")
        print_board(board)
    else:
        print("No solution exists for the given Sudoku board.")

    data_store.save("result.json")
