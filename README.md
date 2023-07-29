# Sudoku-solver-project

Sudoku-solver-project is a project written for AUA AI class.
We implemented a couple of different algorithms and visualisation for them.

## Installation

If you are not gonna use the batch_runner.py, than you only need Python!

Otherwise use the package manager [pip](https://pip.pypa.io/en/stable/) to install tqdm.

```bash
pip install tqdm
```

## Usage
To run each algorithm for first 50 puzzles:

```bash
$ python backend/batch_runner.py
```

To run the frontend:

At Sudoku-solver-project directory run:


```bash
$ python -m http.server
```

Don't close this terminal until you are done with the frontend.

An example puzzle to put in the input, other wise you can run
```
070000043040009610800634900094052000358460020000800530080070091902100005007040802
```

Please not that you can't really switch between Autoplay and back DURING the puzzle.

### If you want to try something else
You can either take an other example from `backend/data/sudoku_data.txt` or
Generate you own (it the same format) modify batch_runner.py or just delete evertything else
from `backend/data/sudoku_data.txt` (So the script won't waste time calculating those) and put
you example ther in one line.

### if something doesn't work
Email Sayat and I will quickly help you.
(Not putting the email publicly on GitHub 
if you are from AUA it's fairly easy to figure out)
