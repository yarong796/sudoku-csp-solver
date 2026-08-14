# sudoku-csp-solver

A Sudoku solver. The program models Sudoku as a constraint satisfaction problem (CSP) and combines AC-3 constraint propagation with backtracking search and variable/value selection heuristics.

## Approach

- Represents each Sudoku cell as a CSP variable with a domain of possible values
- Applies AC-3 to propagate constraints and reduce domains
- Uses Minimum Remaining Values (MRV) to select the next variable
- Uses Least Constraining Value (LCV) to order candidate values
- Uses backtracking search when constraint propagation alone cannot complete the puzzle
- Validates the completed board before returning a solution

The combined approach solves easy puzzles almost immediately and handles more difficult, low-clue puzzles substantially more efficiently than pure backtracking.
