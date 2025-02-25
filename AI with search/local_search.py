# Task 1. 
# Generate an n-queens board using numpy arrays.
# You can implement this any other way you like.
#
# Here we store the row number for the queen in each column, using 0-indexing
# i.e. board[2]=5 means that the queen in the 3rd column is in the 6th row

import numpy as np
rng = np.random.default_rng(seed=2024)

def place_queens(n=8):
  queens = np.array([rng.integers(n) for _ in range(n)])
  return queens

# Here is a quick demo with boards of size 3 to 10 and a hint for checking horizontal clashes
for n in range(3,11):
  board = place_queens(n)
  print(board)

# let's do a quick check to see if there are horizontal clashes
  for col in range(n):
    # count columns with same value as ours (incudes our col)
    matches = np.count_nonzero(board==board[col])
    if matches>1:
      print(f"column {col} clashes horizontally :-(")


def count_coflicts(board):
  n = len(board);
  conflicts =0;


  for col1 in range(n): #iterating over each queen
    for col2 in range(col1 +1, n): #compare with all queens
        row1, row2 = board[col1], board[col2]

        if row1==row2:
          conflicts+=1 #row conflict

        if abs(col1 - col2) == abs(row1 - row2):  #diagonal conflict
          conflicts += 1

  return conflicts

print("Conflicts:", count_coflicts(board) )

def neighbourhood(board):
  n=len(board)
  col = np.random.randint(n) #select random col
  new_board = board.copy()
  new_row = np.random.randint(n) #select new row

  while new_row == board[col]:  #ensuring a different row
        new_row = np.random.randint(n)

  new_board[col] = new_row

  return new_board

# Task 2. Implement a simple hill-climbing local search for the n-queens problem.
def hill_climbing(n):
  board = np.random.randint(n, size=n) #random board
  current_conflicts = count_coflicts(board)

  while True:
    best_board = None
    best_conflicts = current_conflicts

    for _ in range(10): #trying 10 random neighbours
      new_board = neighbourhood(board)
      new_conflicts = count_coflicts(new_board) #recalculate conflicts

      if new_conflicts < best_conflicts: #move if better
        best_board = new_board
        best_conflicts = new_conflicts

    if best_board is None: #stop if no improvement
      break

    board = best_board #move to better board
    current_conflicts = best_conflicts

  return board, current_conflicts
solution, conflicts = hill_climbing(n)
print("Final Board:", solution)
print("Conflicts:", conflicts)
