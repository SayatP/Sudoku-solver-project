from queue import Queue
from copy import copy

from choose_empty_cell import find_empty_cell

from shared.board import Board
from shared.validation import get_domains_for_all_empty_cells

from shared.output import print_board, SolveData

global STEP
STEP = 0


def ac3(board):

    def revise(X1, X2):
        revised = False
        to_remove = set()
        for value in domains[X1]:
            if len(domains[X2] - {value,}) == 0:
                 to_remove.add(value)
                 revised = True
        if revised:
            domains[X1] = domains[X1] - to_remove
        
        return revised

    queue = Queue()
    domains, valid = get_domains_for_all_empty_cells(board)

    if not valid:

        return None

    for key in domains.keys():
        row, col = key
        for ni, nj in board.get_neighbors(row, col):
           if board.getItem(ni, nj) == 0:
               queue.put(((row, col), (ni, nj))) 

    while not queue.empty():
        X1, X2 = queue.get()
        
        if revise(X1, X2):
            if len(domains[X1]) == 0:
                return None
            else:
                for ni, nj in board.get_neighbors(X1[0], X1[1]):
                    if board.getItem(ni, nj) == 0:
                        queue.put(((ni, nj), (X1[0], X1[1]))) 

    return domains




def solve_sudoku(board: Board, data_store):
    global STEP
    data_store.store(STEP)

    empty_cell = find_empty_cell(board)

    if not empty_cell:
        return True  # The board is already filled, so it's solved

    row, col = empty_cell
    domains = ac3(board)

    if not domains:
        return False


    for cell, values in domains.items():
        if len(values) == 1:
            row, col = cell
            board.setItem(row, col, next(iter(values)))
            STEP += 1
            if solve_sudoku(board, data_store):
                return True
            else:
                board.setItem(row, col, 0)
                return False

    for cell, values in domains.items():
        row, col = cell
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

    print(STEP)
    data_store.save("result.json")
