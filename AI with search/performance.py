#Analysing performance by examining:
# the number of nodes expanded,
# the number of nodes that ever appear in the fringe,
# the solution cost (total cost of the path from initial state to solution).
# Run both the A* and ID searches on a set of tasks (i.e. not just A to J) and compare their performance.
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
