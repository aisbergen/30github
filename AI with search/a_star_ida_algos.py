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

