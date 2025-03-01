#a simple hill-climbing local search for the n-queens problem

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
