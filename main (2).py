import sys
from collections import deque

def read_sudoku_from_stdin():
    board = []
    for _ in range(9):
        line = sys.stdin.readline().strip()
        if not line:
            break
        row_values = list(map(int, line.split()))
        board.append(row_values)
    return board

def print_sudoku_solution(board):
    for row in board:
        print(" ".join(map(str, row)))

def validate_solution(board):
    for r in range(9):
        if set(board[r]) != set(range(1,10)):
            return False

    for c in range(9):
        col_vals = [board[r][c] for r in range(9)]
        if set(col_vals) != set(range(1,10)):
            return False

    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            box_vals = []
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    box_vals.append(board[r][c])
            if set(box_vals) != set(range(1,10)):
                return False

    return True

def solve_sudoku_pure_backtracking(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True
    r, c = empty_cell

    for val in range(1, 10):
        if is_valid_pure(board, r, c, val):
            board[r][c] = val
            if solve_sudoku_pure_backtracking(board):
                return True
            board[r][c] = 0

    return False

def find_empty_cell(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None

def is_valid_pure(board, row, col, val):
    if val in board[row]:
        return False

    for r in range(9):
        if board[r][col] == val:
            return False

    box_r = (row // 3) * 3
    box_c = (col // 3) * 3
    for rr in range(box_r, box_r + 3):
        for cc in range(box_c, box_c + 3):
            if board[rr][cc] == val:
                return False

    return True

def create_csp(board):
    domains = {}
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                domains[(r, c)] = set(range(1, 10))
            else:
                domains[(r, c)] = {board[r][c]}
    neighbors = {}
    for r in range(9):
        for c in range(9):
            nset = set()
            for cc in range(9):
                if cc != c:
                    nset.add((r, cc))
            for rr in range(9):
                if rr != r:
                    nset.add((rr, c))
            box_r = (r // 3) * 3
            box_c = (c // 3) * 3
            for rr in range(box_r, box_r + 3):
                for cc in range(box_c, box_c + 3):
                    if (rr, cc) != (r, c):
                        nset.add((rr, cc))
            neighbors[(r, c)] = nset

    return domains, neighbors

def revise(domains, xi, xj):

    if len(domains[xj]) == 1:
        sole_val = next(iter(domains[xj]))
        if sole_val in domains[xi]:
            domains[xi].remove(sole_val)
            return True
    return False

def ac3(domains, neighbors, queue, saved):

    while queue:
        xi, xj = queue.popleft()
        old_domain_xi = domains[xi].copy()
        if revise(domains, xi, xj):

            saved.append((xi, old_domain_xi))
            if len(domains[xi]) == 0:
                return False

            for xk in neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def get_lcv_values(var, domains, neighbors):
    result = []
    for val in domains[var]:
        count = 0
        for nbr in neighbors[var]:
            if val in domains[nbr]:
                count += 1
        result.append((val, count))
    result.sort(key=lambda x: x[1])
    return [val for (val, _) in result]

def backtracking_search(domains, neighbors):

    if all(len(domains[v]) == 1 for v in domains):
        return {v: next(iter(domains[v])) for v in domains}

    var = min((v for v in domains if len(domains[v]) > 1),
              key=lambda v: len(domains[v]))

    for val in get_lcv_values(var, domains, neighbors):
        saved = []
        old_domain = domains[var].copy()
        domains[var] = {val}
        saved.append((var, old_domain))

        queue = deque()
        for nbr in neighbors[var]:
            queue.append((nbr, var))

        if ac3(domains, neighbors, queue, saved):
            result = backtracking_search(domains, neighbors)
            if result is not None:
                return result

        # Backtrack
        while saved:
            v, old_dom = saved.pop()
            domains[v] = old_dom

    return None

def solve_sudoku_ac3(board):

    domains, neighbors = create_csp(board)

    init_queue = deque()
    for x in neighbors:
        for y in neighbors[x]:
            init_queue.append((x, y))
    if not ac3(domains, neighbors, init_queue, saved=[]):
        return None

    assignment = backtracking_search(domains, neighbors)
    if assignment is None:
        return None

    solved_board = [[0]*9 for _ in range(9)]
    for (r, c), val in assignment.items():
        solved_board[r][c] = val
    return solved_board

def main():
    board = read_sudoku_from_stdin()
    if len(board) < 9 or any(len(row) < 9 for row in board):
        print("No solution.")
        return

    solution = solve_sudoku_ac3(board)

    if solution and validate_solution(solution):
        print_sudoku_solution(solution)
    else:
        print("No solution.")

if __name__ == "__main__":
    main()
