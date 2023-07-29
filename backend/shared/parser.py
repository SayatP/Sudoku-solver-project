def parse_puzzle(puzzle):
    "Parse from Kaggle format"
    matrix = []
    for i in range(0, 73, 9):
        matrix.append(list(map(int, puzzle[i : i + 9])))
    return matrix
