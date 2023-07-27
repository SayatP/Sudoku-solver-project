class Cell:
    def __init__(self, state):
        self.state = state
        if state == 0:
            self.modifiable = True
        else:
            self.modifiable = False
        self.domain = [None for _ in range(9)]

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def modifiable(self):
        return self.modifiable

    def set_modifiable(self, modifiable):
        self.modifiable = modifiable


class Board:

    def __init__(self, data):
        self.data = [[Cell(element) for element in row] for row in data]

    def getItem(self, i, j):
        return self.data[i][j].get_state()

    def getCell(self, i, j):
        return self.data[i][j]

    def setItem(self, i, j, val):
        self.data[i][j].set_state(val)

    def get_current_state(self):
        return self.data

    # Define the __eq__ method for equality comparison
    def __eq__(self, other):
        return 0

    # Define the __lt__ method for less-than comparison
    def __lt__(self, other):
        return 0

    def get_unwrapped_state(self):
        return [[element.get_state() for element in row] for row in self.data]

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
