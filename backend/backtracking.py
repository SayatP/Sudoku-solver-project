from shared.validation import find_empty_cell

from shared.board import Board
from shared.validation import get_basic_domain, get_domains_for_all_empty_cells

from shared.store import print_board, SolveDataStore
from shared.parser import parse_puzzle

NAME = "backtracking"


def backtracking(board: Board, data_store, domains, STEP):
    empty_cell = find_empty_cell(board)

    if not empty_cell:
        return True

    row, col = empty_cell

    domain = get_basic_domain(board, row, col)

    for value in sorted(domain):
        board.setItem(row, col, value)
        STEP += 1

        data_store.store(STEP, domains=domains)

        if backtracking(board, data_store, domains, STEP):
            return True

        board.setItem(row, col, 0)
        STEP += 1

        data_store.store(STEP, domains=domains)

    return False


def main(puzzle):
    STEP = 0

    input_board = parse_puzzle(puzzle)
    board = Board(input_board)
    domains, _ = get_domains_for_all_empty_cells(board)

    data_store = SolveDataStore(board)
    if backtracking(board, data_store, domains, STEP):
        print("Sudoku solved:")
        print_board(board)
    else:
        print("No solution exists for the given Sudoku board.")

    data_store.save("./" + "backend/data/" + NAME + "/" + puzzle + ".json")
