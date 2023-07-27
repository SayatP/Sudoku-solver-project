import tqdm
import time
import json

from mac import main as mac
from backtracking import main as backtracking
from backtracking_ac3 import main as backtracking_ac3
from backtracking_mrv import main as backtracking_mrv

with open("backend/data/sudoku_data.txt") as f:
    puzzles = [i.strip() for i in f.readlines()]



print(len(puzzles))
exit()
algos = {
    "mac": mac,
    "backtracking": backtracking,
    "backtracking_ac3": backtracking_ac3,
    "backtracking_mrv": backtracking_mrv,
}


results = {
    "mac": {},
    "backtracking": {},
    "backtracking_ac3": {},
    "backtracking_mrv": {},
}

for k, v in algos.items():
    global_start = time.time()
    for puzzle in tqdm.tqdm(puzzles[:500]):
        # backtracking(puzzle)
        # backtracking_ac3(puzzle)
        t1 = time.time()
        v(puzzle)
        t2 = time.time()
        results[k][puzzle] = t2-t1


    global_end = time.time()
    results[k]["time_for_1000"] = global_end - global_start

    with open("results.json", "w") as f:
        json.dump(results, f)