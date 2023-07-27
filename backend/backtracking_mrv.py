from choose_empty_cell import find_empty_cell

from shared.board import Board
from shared.validation import get_basic_domain, get_domains_for_all_empty_cells

from shared.store import print_board, SolveDataStore
from shared.parser import parse_puzzle

NAME = "backtracking_mrv"


def backtracking(board: Board, data_store, domains, STEP):

    empty_cell = find_empty_cell(board)

    if not empty_cell:
        return True  # The board is already filled, so it's solved



    domains, valid = get_domains_for_all_empty_cells(board)

    if not valid:
        return False

    for k in sorted(domains, key=lambda k: len(domains[k])): #MRV

        domain = domains[k]
        for value in sorted(domain):
            board.setItem(k[0], k[1] , value)
            STEP += 1

            data_store.store(STEP, domains=domains)


            if backtracking(board, data_store, domains, STEP):
                return True

            # Backtrack if the current number didn't lead to a solution
            board.setItem(k[0], k[1], 0)
            STEP += 1

            data_store.store(STEP, domains=domains)

    return False



# So far, backtracking is the only one who managed to "solve" this in resonable time

# input_board = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
# ]


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


# example = "070000043040009610800634900094052000358460020000800530080070091902100005007040802"
# example_extra = "000006300000200005080000000006200040000000010000090000910080000000600078000000090"
example_hard = "009073000607000008000800937092008654053649172000125800700000010004000009968302000"

# example_extra_hard = "500200040000603000030009007003007000007008000600000020080000003000400600000100500"
# zeros = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'

main(example_hard)
