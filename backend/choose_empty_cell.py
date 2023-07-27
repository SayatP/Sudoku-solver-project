from shared.validation import get_basic_domain


def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board.data[i][j] == 0:
                return i, j

    return None


def find_empty_cell_least_constrained(board):
    # TODO refactor
    for i in range(9):
        for j in range(9):
            if len(get_basic_domain(board, i, j)) == 1:
                return i, j

    return find_empty_cell(board)
