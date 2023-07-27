from choose_empty_cell import find_empty_cell

from shared.board import Board
from shared.validation import get_basic_domain

from shared.output import print_board, SolveData

global STEP
STEP = 0


def solve_sudoku(board: Board, data_store):
    global STEP
    data_store.store(STEP)

    empty_cell = find_empty_cell(board)

    if not empty_cell:
        return True  # The board is already filled, so it's solved

    row, col = empty_cell

    domain = get_basic_domain(board, row, col)
    for value in domain:
        board.setItem(row, col, value)
        STEP += 1
        if solve_sudoku(board, data_store):
            return True

        # Backtrack if the current number didn't lead to a solution
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
