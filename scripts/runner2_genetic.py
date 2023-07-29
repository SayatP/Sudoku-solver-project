import tqdm
import time
import json

import multiprocessing

from mac import main as mac
from backtracking import main as backtracking
from backtracking_ac3 import main as backtracking_ac3
from backtracking_mrv import main as backtracking_mrv

from genetic import main as genetic

TIMEOUT = 5

with open("backend/data/sudoku_data.txt") as f:
    puzzles = [i.strip() for i in f.readlines()]


results = {}

global_start = time.time()
for puzzle in tqdm.tqdm(puzzles):
    terminated = False
    t1 = time.time()
    p = multiprocessing.Process(target=genetic, args=(puzzle,))
    p.start()
    p.join(TIMEOUT)

    if p.is_alive():
        print("function terminated")
        terminated = True
        p.terminate()
        p.join()

    t2 = time.time()
    if not terminated:
        results[puzzle] = t2 - t1
    else:
        results[puzzle] = 0


global_end = time.time()
results["time_for_1000"] = global_end - global_start

with open("results_genetic_final.json", "w") as f:
    json.dump(results, f)
