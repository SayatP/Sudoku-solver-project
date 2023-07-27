def is_valid(board_data, row, col, num):
    # Check if the number is not already present in the row
    if num in board_data[row]:
        return False

    # Check if the number is not already present in the column
    try:
        if num in [board_data[i][col] for i in range(9)]:
            return False
    except Exception:
        import pdb

        pdb.set_trace()

    # Check if the number is not already present in the 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board_data[start_row + i][start_col + j] == num:
                return False

    return True


def get_basic_domain(board, row, col):
    domain = [i for i in range(1, 10) if is_valid(board.data, row, col, i)]
    board.setDomain(row, col, domain)
    return domain

def get_domains_for_all_empty_cells(board):
    domains = {}
    # set base domains
    for row in range(9):
        for col in range(9):
            if board.getItem(row, col) == 0:
                domain = get_basic_domain(board, row, col)
                if len(domain) == 0:
                    return None, False
                domains[(row, col)] = set(domain)

    return domains, True
