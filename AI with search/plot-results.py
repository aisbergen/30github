import numpy as np
import matplotlib.pyplot as plt

def place_queens(n=100):
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

  fitness_progress = []  # Track current fitness
  best_fitness_progress = []  # Track best fitness found
  best_fitness = current_conflicts  # Start with initial fitness as best

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

      #track progress
      fitness_progress.append(old_conflicts) #store current fitness
      best_fitness = min(best_fitness, old_conflicts) #update
      best_fitness_progress.append(best_fitness)

      T = T * 0.99 #Exponential Cooling (decreasing temp)
      if T < 1e-10:  #Stop if temperature is too low
            break

    if best_board is None: #stop if no improvement
      break

    board = best_board #move to better board
    current_conflicts = old_conflicts

  return board, current_conflicts, fitness_progress, best_fitness_progress
print("Final Board:", solution)
print("Conflicts:", conflicts)

n=100
solution, conflicts, fitness_progress, best_fitness_progress = simulated_annealing(n)


#Plot fitness progress
plt.figure(figsize=(10, 5))
plt.plot(label="Current Fitness", color="blue")
plt.plot(best_fitness_progress, label="Best Fitness", color="red", linestyle="dashed")
plt.xlabel("Iterations")
plt.ylabel("Conflict Count (Fitness)")
plt.title(f"Simulated Annealing: Fitness Progress (n={n})")
plt.legend()
plt.show()


def hill_climbing(n=8):
  board = np.random.randint(n, size=n) #random board
  current_conflicts = count_conflicts(board)

  while True:
    best_board = None
    best_conflicts = current_conflicts

    for _ in range(10): #trying 10 random neighbours
      new_board = neighbourhood(board)
      new_conflicts = count_conflicts(new_board) #recalculate conflicts

      if new_conflicts < best_conflicts: #move if better
        best_board = new_board
        best_conflicts = new_conflicts

    if best_board is None: #stop if no improvement
      break

     #track progress
    fitness_progress.append(current_conflicts) #store current fitness
    best_fitness = min(best_conflicts, current_conflicts) #update
    best_fitness_progress.append(best_fitness)

    board = best_board #move to better board
    current_conflicts = best_conflicts

  return board, current_conflicts, fitness_progress, best_fitness_progress

solution, conflicts, fitness_progress, best_fitness_progress = hill_climbing(n)
print("Final Board:", solution)
print("Conflicts:", conflicts)

n=8
solution, conflicts, fitness_progress, best_fitness_progress = hill_climbing(n)

plt.figure(figsize=(10, 5))
plt.plot(label="Current Fitness", color="black")
plt.plot(best_fitness_progress, label="Best Fitness", color="blue")
plt.xlabel("Iterations")
plt.ylabel("Conflict Count (Fitness)")
plt.title(f"Hill Climbing: Fitness Progress (n={n})")
plt.legend()
plt.show()
