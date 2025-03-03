def place_queens(n=8):
  queens = np.array([rng.integers(n) for _ in range(n)])
  return queens

def count_conflicts(board):
  n = len(board);
  conflicts =0;

  for col1 in range(n): #iterating over each queen
    for col2 in range(col1 +1, n): #compare only unique pairs
        row1, row2 = board[col1], board[col2]

        if row1==row2:
          conflicts+=1 #row conflict

        if abs(col1 - col2) == abs(row1 - row2):  #diagonal conflict
          conflicts += 1

  return conflicts

print("Conflicts:", count_conflicts(board) )

def simulated_annealing(n, T=100, max_steps=1000):
  board = place_queens(n) #random board
  current_conflicts = count_conflicts(board)

  while True:
    best_board = None
    old_conflicts = current_conflicts

    for step in range(max_steps): #trying 10 random neighbours
      new_board = neighbourhood(board)
      new_conflicts = count_conflicts(new_board) #recalculate conflicts

      if new_conflicts < old_conflicts: #move if better
        best_board = new_board
        old_conflicts = new_conflicts

      if new_conflicts > old_conflicts:
        delta_E = new_conflicts - old_conflicts  #Conflict increase
        accept_prob = np.exp(-delta_E / T)  # Acceptance probability
        if np.random.rand() < accept_prob:  # Sometimes accept worse move
            board, old_conflicts = new_board, new_conflicts

      T = T * 0.99 #Exponential Cooling (decreasing temp)
      if T < 1e-10:  #Stop if temperature is too low
            break

    if best_board is None: #stop if no improvement
      break

    board = best_board #move to better board
    current_conflicts = old_conflicts

  return board, current_conflicts
solution, conflicts = simulated_annealing(n)
print("Final Board:", solution)
print("Conflicts:", conflicts)
