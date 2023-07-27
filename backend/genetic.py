import threading
from genetic_algorithm_model.board import Board
from shared.store import print_board, SolveDataStore
from shared.parser import parse_puzzle
import random

NAME = "genetic"


def is_valid(board, row, col, num):
    # Check if placing 'num' in the given position (row, col) is valid
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def is_valid_candidate(board, row, col, num):
    # Check if placing 'num' in the given position (row, col) is valid

    for i in range(9):
        if ((not board.getCell(row, i).modifiable) and board.getItem(row, i) == num) \
                or ((not board.getCell(i, col).modifiable) and board.getItem(i, col) == num):
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board.getItem(start_row + i, start_col + j) == num and board.getCell(start_row + i,
                                                                                    start_col + j).modifiable == False:
                return False
    return True


def print_board(board):
    for row in board.get_current_state():
        print(' '.join(str(num.get_state()) for num in row))


def createIndividual(board):
    # Create an empty 9x9 Sudoku board
    newBoard = Board([[0 for _ in range(9)] for _ in range(9)])
    for i in range(9):
        for j in range(9):
            itemInBoard = board.getItem(i, j)
            if itemInBoard == 0:
                candidate = random.randint(1, 9)
                while (not is_valid_candidate(board, i, j, candidate)):
                    candidate = random.randint(1, 9)
                newBoard.setItem(i, j, candidate)
                newBoard.getCell(i, j).set_modifiable(True)
            else:
                newBoard.setItem(i, j, itemInBoard)
    return newBoard


# Function to evaluate fitness of boards in separate threads
def evaluate_fitness_in_threads(population):
    fitness_values = [None] * len(population)

    # Function to evaluate the fitness of a board in a separate thread
    def evaluate_board_fitness(index, board):
        fitness_values[index] = evaluate_fitness(board)

    # Create and start a separate thread for each board
    threads = []
    for i, board in enumerate(population):
        thread = threading.Thread(target=evaluate_board_fitness, args=(i, board))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return fitness_values


def genetic_algorithm_solver(board):
    # Initialize a population of random Sudoku boards
    for i in range(1):
        print(str(i + 1) + "th try")
        population = [createIndividual(board) for _ in range(1000)]
        for generation in range(100):
            # Evaluate fitness of each board in the population (lower is better)
            fitness_scores = evaluate_fitness_in_threads(population)
            # [evaluate_fitness(board) for board in population]

            # Select the best-performing boards to form the next generation
            best_boards = select_best_boards(population, fitness_scores)
            print(sorted(fitness_scores)[0])
            # Perform crossover and mutation to create the next generation
            population = create_next_generation(best_boards)

            # Check if any board is solved
            for board in population:
                if is_solved(board):
                    print("Sudoku is solved")
                    data_store = SolveDataStore(population[0])
                    data_store.save_board(population[0].get_unwrapped_state(), "result.json")
                    return board

        print("Not solved, best approximation")
        data_store = SolveDataStore(population[0])
        data_store.save_board(population[0], "result.json")
        return population[0]  # No solution found within the given number of generations


def evaluate_fitness(board):
    # Count the number of conflicts in each row, column, and 3x3 box
    data = board.get_unwrapped_state()
    conflicts = 0
    for i in range(9):
        for j in range(9):
            if data[i].count(data[i][j]) > 1:
                conflicts += 1
            if [data[x][j] for x in range(9)].count(data[i][j]) > 1:
                conflicts += 1
            start_row, start_col = 3 * (i // 3), 3 * (j // 3)
            if [data[start_row + x][start_col + y] for x in range(3) for y in range(3)].count(data[i][j]) > 1:
                conflicts += 1

    return conflicts


def select_best_boards(population, fitness_scores):
    # Select the best-performing boards based on their fitness scores
    sorted_boards = [board for _, board in sorted(zip(fitness_scores, population))]
    return sorted_boards[:len(sorted_boards) // 3]


def create_next_generation(boards):
    # Create the next generation through crossover and mutation
    next_generation = []
    for _ in range(700):  # Creating 50 new boards
        parent1, parent2 = random.sample(boards, 2)
        child = crossover(parent1.get_unwrapped_state(), parent2.get_unwrapped_state())
        mutate(Board(child))

        next_generation.append(Board(child))

    return next_generation


def create_empty_board():
    return [[0 for _ in range(9)] for _ in range(9)]


def crossover(parent1, parent2):
    child = create_empty_board()
    for i in range(9):
        for j in range(9):
            if random.random() < 0.5:
                child[i][j] = parent1[i][j]
            else:
                child[i][j] = parent2[i][j]

    return child


def mutate(board):
    # Perform mutation to change a cell's value randomly
    row, col = random.randint(0, 8), random.randint(0, 8)
    num = random.randint(1, 9)
    if is_valid(board.get_unwrapped_state(), row, col, num):
        board.setItem(row, col, num)


def is_solved(board):
    # Check if a board is solved (no empty cells)
    return evaluate_fitness(board) == 0


# #
# # Example Sudoku board (0 represents empty cells)
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
#
# if __name__ == "__main__":
#     board = Board(input_board)
#     print_board(genetic_algorithm_solver(board))


def main(puzzle):
    input_board = parse_puzzle(puzzle)
    board = Board(input_board)
    data_store = SolveDataStore(board)
    print_board(genetic_algorithm_solver(board))
    data_store.save("./" + NAME + "/" + puzzle + ".json")


example = "070000043040009610800634900094052000358460020000800530080070091902100005007040802"

example_extra = "000006300000200005080000000006200040000000010000090000910080000000600078000000090"
example_hard = "009073000607000008000800937092008654053649172000125800700000010004000009968302000"

example_sayat = "500200040000603000030009007003007000007008000600000020080000003000400600000100500"

zeros = "000000000000000000000000000000000000000000000000000000000000000000000000000000000"
# main(example_hard)
