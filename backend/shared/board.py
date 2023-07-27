class Board:
    def __init__(self, data):
        self.data = data
        self.domains = [[None for _ in range(9)] for _ in range(9)]

    def getItem(self, i, j):
        return self.data[i][j]

    def setItem(self, i, j, val):
        self.data[i][j] = val
        self.domains[i][j] = None

    def get_current_state(self):
        return self.data

    def get_neighbors(self, i, j):
        neighbors = []
        for k in range(9):
            if k != i:
                neighbors.append((k, j))
            if k != j:
                neighbors.append((i, k))

        box_i, box_j = 3 * (i // 3), 3 * (j // 3)
        for x in range(box_i, box_i + 3):
            for y in range(box_j, box_j + 3):
                if (x, y) != (i, j):
                    neighbors.append((x, y))

        return neighbors
