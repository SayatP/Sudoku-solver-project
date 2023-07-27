from queue import Queue
from copy import deepcopy

from choose_empty_cell import find_empty_cell

from shared.board import Board
from shared.validation import get_domains_for_all_empty_cells

from shared.store import print_board, SolveDataStore
from shared.parser import parse_puzzle


NAME = "backtracking_ac3"

def ac3(board, data_store, STEP):

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
            STEP += 1
            data_store.store(STEP, domains)

    return domains, STEP


def backtracking_with_ac3(board: Board, data_store: SolveDataStore, domains, STEP):
    empty_cell = find_empty_cell(board)

    if not empty_cell:
        return True, STEP  # The board is already filled, so it's solved

    row, col = empty_cell


    if not domains:
        return False, STEP

    data_store.store(STEP, domains)

    for cell, values in domains.items():
        if len(values) == 1:
            row, col = cell
            board.setItem(row, col, next(iter(values)))
            STEP += 1

            local_domains = deepcopy(domains)
            local_domains.pop(cell)
            result, STEP = backtracking_with_ac3(board, data_store, local_domains, STEP)
            if result:
                data_store.store(STEP, domains)
                return True, STEP
            else:
                board.setItem(row, col, 0)
                return False, STEP

    for cell, values in domains.items():
        row, col = cell
        for value in values:
            board.setItem(row, col, value)
            STEP += 1
            local_domains = deepcopy(domains)
            local_domains.pop(cell)
            result, STEP = backtracking_with_ac3(board, data_store, local_domains, STEP)
            if result:
                return True, STEP

            board.setItem(row, col, 0)

    data_store.store(STEP, domains)
    return False, STEP


# Example Sudoku board (0 represents empty cells)
# input_board = [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9],
# ]



# if __name__ == "__main__":
#     board = Board(input_board)
#     data_store = SolveDataStore(board)
#     if backtracking_with_ac3(board, data_store):
#         print("Sudoku solved:")
#         print_board(board)
#     else:
#         print("No solution exists for the given Sudoku board.")

#     data_store.save("result.json")


def main(puzzle):
    global STEP
    STEP = 0
    input_board = parse_puzzle(puzzle)
    board = Board(input_board)
    data_store = SolveDataStore(board)
    domains, STEP = ac3(board, data_store, STEP)

    if backtracking_with_ac3(board, data_store, domains, STEP):
        print("Sudoku solved:")
        print_board(board)
    else:
        print("No solution exists for the given Sudoku board.")

    data_store.save("./" + "backend/data/" + NAME + "/" + puzzle + ".json")


# example = "070000043040009610800634900094052000358460020000800530080070091902100005007040802"

# example_extra = "000006300000200005080000000006200040000000010000090000910080000000600078000000090"
# example_hard = "009073000607000008000800937092008654053649172000125800700000010004000009968302000"

# example_sayat = "500200040000603000030009007003007000007008000600000020080000003000400600000100500"

# zeros = "000000000000000000000000000000000000000000000000000000000000000000000000000000000"
# main(example_hard)
