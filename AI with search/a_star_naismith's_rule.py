#The rule states that it takes 1 hour to walk 5 km, with an extra hour added for each 600m of climbing. So, if you were to
#walk up a hill that was precisely 5km long, but with a gradient of 12%, it should take you 2 hours to complete.

import heapq

def neighbours(n):
    """Return a list of (neighbor, cost, elevation change)"""
    return [(b, d, elevations[b] - elevations[n]) for (a, b, d) in paths if a == n] + \
           [(a, d, elevations[a] - elevations[n]) for (a, b, d) in paths if b == n]


def heuristic(node, goal):
    """Estimate time to goal using Naismith’s Rule."""
    sld_time = sld_dists[node] / 5  # Walking time
    elevation_change = elevations[goal] - elevations[node]  # Elevation difference
    climb_time = max(0, elevation_change / 600)  # Extra time for climbing
    return sld_time + climb_time  # Total estimated time

def a_search(n_from, n_to):
    """A* Search Algorithm using Naismith’s Rule"""
    frontier = []
    heapq.heappush(frontier, (0, n_from))  # Priority queue based on f(n)
    
    g_costs = {city: float('inf') for city in sld_dists}
    g_costs[n_from] = 0  #Start city has cost 0
    came_from = {}  #Stores parent nodes for path reconstruction

    while frontier:
        current_f, current_node = heapq.heappop(frontier)
        
        if current_node == n_to:  #Goal reached
            return reconstruct_path(came_from, n_to)
        
        for neighbor, cost, elevation_change in neighbours(current_node):  
            walk_time = cost / 5  #Walking time
            climb_time = max(0, elevation_change / 600)  # Extra time for climbing
            new_g = g_costs[current_node] + walk_time + climb_time

            if new_g < g_costs[neighbor]:  #Found a better path
                g_costs[neighbor] = new_g
                f_value = new_g + heuristic(neighbor, n_to)  #A* heuristic
                heapq.heappush(frontier, (f_value, neighbor))
                came_from[neighbor] = current_node  #Store parent

    return None  #No path found

def reconstruct_path(came_from, current):
    """Reconstructs path from goal to start using came_from dictionary"""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)
    return path

# Define straight-line distances (SLD)
sld_dists = {'A': 0, 'B': 200, 'C': 600, 'D': 100, 'E': 300,
             'F': 300, 'G': 100, 'H': 500, 'I': 400, 'J': 500}

# Define elevation levels for each city
elevations = {'A': 0, 'B': 200, 'C': 600, 'D': 100, 'E': 300,
              'F': 300, 'G': 100, 'H': 500, 'I': 400, 'J': 500}

# Define graph (edges)
paths = [('A', 'B', 5), ('A', 'C', 5), ('B', 'F', 5), ('C', 'D', 5),
         ('D', 'E', 5), ('D', 'F', 10), ('E', 'G', 10), ('E', 'H', 5),
         ('F', 'I', 5), ('G', 'H', 5), ('H', 'J', 5), ('I', 'J', 5)]

# Run A* from A to J
path = a_search('A', 'J')
print("Shortest Path:", path)
