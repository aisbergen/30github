#################
# ORIGINAL DATA #
#################

# imaginative place names A, B, ..., J
# a quick trick: split the string into individual letters
p_names = [c for c in 'ABCDEFGHIJ']
print(f"Our places are called:\n{p_names}")

# the original problem supplied a triangular half of the distance matrix:
sld_tri = [
  [0,3,3,3,7,7,11,11,15,15],[0,7,3,7,3,7,11,11,15],[0,3,3,11,15,7,15,15],[0,3,7,7,7,15,15],
  [0,11,7,3,11,11],[0,3,7,3,7],[0,3,3,3],[0,7,3],[0,3],[0]
]

# the walking distances (where possible) between points,
# e.g. (0,2,5) means from A (index 0) to C (index 2) there's a 5 km path
paths = [(0,1,5), (0,2,5), (0,3,5), (1,5,5), (2,4,5), (3,4,5), (3,5,10),
         (4,6,10), (4,7,5), (5,8,5), (6,7,5), (6,9,5), (7,9,5), (8,9,5)]

# the elevations of the places A..J:
elevations = [0, 200, 600, 100, 300, 300, 100, 500, 400, 500]

# it might be clearer if we convert the triangle to a  full distance matrix:
n_places = len(sld_tri)
sld_dists = np.zeros((n_places,n_places))
for i in range(n_places):
  for j in range(n_places-i):
    d = sld_tri[i][j]
    sld_dists[i,i+j] = d
    sld_dists[i+j,i] = d
print(f"The straight-line distances are:\n{sld_dists}")

#Task 1. A* Search with SLD Heuristic

import heapq

def a_search(n_from, n_to, f_value=0, cutoff_level=1000, debug=False):
    """A* Search Algorithm with SLD Heuristic"""
    frontier = []
    heapq.heappush(frontier, (f_value, n_from))  # Priority queue
    
    g_costs = {city: float('inf') for city in p_names}
    g_costs[n_from] = 0  # Start city has cost 0
    
    came_from = {}  # Stores parent nodes for path reconstruction

    while frontier:
        current_f, current_node = heapq.heappop(frontier)
        
        if current_node == n_to:  # Goal reached
            return reconstruct_path(came_from, current_node)
        
        for neighbor, cost in neighbours(current_node):
            new_g = g_costs[current_node] + cost
            if new_g < g_costs[neighbor]:  # Found a better path
                g_costs[neighbor] = new_g
                f_value = new_g + sld_dists_dict[current_node][n_to]  # A* heuristic
                heapq.heappush(frontier, (f_value, neighbor))
                came_from[neighbor] = current_node  # Store parent

    return None  # No path found

def reconstruct_path(came_from, current):
    """Reconstructs path from goal to start using came_from dictionary"""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)
    return path

# Convert sld_dists into a dictionary
sld_dists_dict = {p_names[i]: {p_names[j]: sld_dists[i][j] for j in range(n_places)} for i in range(n_places)}

# Define neighbors function with place names
def neighbours(n):
    """Return a list of (neighbor_name, cost) pairs"""
    node_index = p_names.index(n)  # Convert name to index
    return [(p_names[b], d) for (a, b, d) in paths if a == node_index] + \
           [(p_names[a], d) for (a, b, d) in paths if b == node_index]

# Run A* from A to D
path = a_search('A', 'J')
print("Shortest Path:", path)

#Task 2. Implement the iterative-deepening search algorithm for our scenario.

def depth_limited_search(node, goal, depth, path):
  if node == goal:
    return path + [node]

  if depth ==0:
    return "CUTOFF" #reached limit

  cutoff_occured = False

  for neighbour, _, in neighbours(node): #explore neighbors
     if neighbour not in path:  # Avoid cycles
          result = depth_limited_search(neighbour, goal, depth - 1, path + [node])

          if result == "CUTOFF":
                cutoff_occurred = True  # We hit the depth limit, so retry at higher depth
          elif result is not None:
                return result
  return "CUTOFF" if cutoff_occurred else None


def ida(start, goal):
  depth = 0

  while True:
     result = depth_limited_search(start, goal, depth, [])

     if result != "CUTOFF":
            return result  # Found the goal or failure

     depth += 1

path = ida('A', 'J')
print("Shortest Path:", path)

#Task 3 Analysing Performance

import heapq

# Convert the SLD matrix into a dictionary mapping place names to distances
sld_dists_dict = {
    p_names[i]: {p_names[j]: float(sld_dists[i, j]) for j in range(n_places)}
    for i in range(n_places)
}

print("SLD Distances Dictionary:\n", sld_dists_dict)


def heuristic(node, goal):
     return sld_dists_dict[node][goal]

print("SLD Distances Dictionary:\n", sld_dists_dict)

def a_star_search(start, goal):
    """A* Search Algorithm with Performance Metrics"""

    frontier = []
    heapq.heappush(frontier, (0, start))  # Priority queue with f(n) values
    came_from = {}  # Tracks the path
    g_costs = {city: float('inf') for city in sld_dists_dict}
    g_costs[start] = 0  # Start city cost is 0

    nodes_expanded = 0
    max_fringe_size = 0

    while frontier:
        max_fringe_size = max(max_fringe_size, len(frontier))  # Track max fringe size
        current_f, current_node = heapq.heappop(frontier)

        nodes_expanded += 1  # Track nodes expanded

        if current_node == goal:
            return reconstruct_path(came_from, start, goal), g_costs[goal], nodes_expanded, max_fringe_size

        for neighbor, cost in neighbours(current_node):
            new_g = g_costs[current_node] + cost

            if new_g < g_costs[neighbor]:  # Found a better path
                g_costs[neighbor] = new_g
                f_value = new_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (f_value, neighbor))
                came_from[neighbor] = current_node  # Store parent

    return None, float('inf'), nodes_expanded, max_fringe_size  # No path found


def depth_limited_search(node, goal, g, threshold, path, nodes_expanded, max_fringe_size):
    """Performs Depth-Limited Search (DLS) up to a given f-cost threshold."""
    nodes_expanded[0] += 1  # Increment nodes expanded count
    max_fringe_size[0] = max(max_fringe_size[0], len(path))  # Track max fringe size

    f = g + heuristic(node, goal)  

    if f > threshold:
        return f  # Cutoff: Return the smallest f-value exceeded

    if node == goal:
        return path + [node], g, nodes_expanded[0], max_fringe_size[0]  # Found the goal, return cost

    min_threshold = float('inf')  # Store the next smallest threshold for IDA*

    for neighbor, cost in neighbours(node):
        if neighbor not in path:  # Avoid cycles
            result = depth_limited_search(
                neighbor, goal, g + cost, threshold, path + [node], nodes_expanded, max_fringe_size
            )

            if isinstance(result, list):  # If result is a successful path
                return result

            if isinstance(result, (int, float)):  # If result is a new threshold
                min_threshold = min(min_threshold, result)

    return min_threshold  # Return the smallest threshold for the next iteration


def ida_search(start, goal):
    """Performs Iterative Deepening A* (IDA*) with Performance Metrics."""
    threshold = heuristic(start, goal)  
    nodes_expanded = [0]  # Mutable counter
    max_fringe_size = [0]  # Mutable counter

    while True:
        result = depth_limited_search(start, goal, 0, threshold, [], nodes_expanded, max_fringe_size)

        if isinstance(result, list):  # Found goal, return path
            return result, nodes_expanded[0], max_fringe_size[0]

        if result == float('inf'):  # No path found
            return "FAILURE", nodes_expanded[0], max_fringe_size[0]

        threshold = result  # Update threshold for next iteration


tasks = [('A', 'J'), ('B', 'H'), ('C', 'G')]

for start, goal in tasks:
    print(f"\n🔹 Comparing A* and IDA for {start} → {goal}")

    # A*
    a_star_path, a_star_cost, a_star_expanded, a_star_fringe = a_star_search(start, goal)
    print(f"A* Path: {a_star_path}, Cost: {a_star_cost}, Expanded: {a_star_expanded}, Max Fringe: {a_star_fringe}")

    # IDA
    ida_path, ida_expanded, ida_fringe = ida_search(start, goal)
    print(f"IDA Path: {ida_path}, Cost: {len(ida_path) - 1 if ida_path else 'N/A'}, Expanded: {ida_expanded}, Max Fringe: {ida_fringe}")
