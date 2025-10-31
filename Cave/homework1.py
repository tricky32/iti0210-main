import time
import os
from queue import Queue, PriorityQueue

# Helper function to calculate Manhattan distance
def manhattan_heuristic(a, b):
    (x1, y1), (x2, y2) = a, b
    return abs(x1 - x2) + abs(y1 - y2)

# Function to find neighboring cells on the map
def neighbors(map_data, current):
    rows, cols = len(map_data), len(map_data[0])
    x, y = current
    possible_moves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    result = []
    for nx, ny in possible_moves:
        if 0 <= nx < rows and 0 <= ny < cols and map_data[nx][ny] != '*':
            result.append((nx, ny))
    return result

# BFS search algorithm with iteration count
def bfs_search(map_data, start, goal):
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None
    iterations = 0  # Track iterations

    while not frontier.empty():
        current = frontier.get()
        iterations += 1  # Increment on each iteration
        if current == goal:
            break
        for next in neighbors(map_data, current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    # Reconstruct the path
    current = goal
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    return path, iterations  # Return the path and number of iterations

# Greedy search algorithm with iteration count
def greedy_search(map_data, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    came_from[start] = None
    iterations = 0  # Track iterations

    while not frontier.empty():
        _, current = frontier.get()
        iterations += 1  # Increment on each iteration
        if current == goal:
            break
        for next in neighbors(map_data, current):
            if next not in came_from:
                priority = manhattan_heuristic(next, goal)
                frontier.put((priority, next))
                came_from[next] = current

    # Reconstruct the path
    current = goal
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    return path, iterations  # Return the path and number of iterations

# A* search algorithm with iteration count
def astar_search(map_data, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    iterations = 0  # Track iterations

    while not frontier.empty():
        _, current = frontier.get()
        iterations += 1  # Increment on each iteration
        if current == goal:
            break

        for next in neighbors(map_data, current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + manhattan_heuristic(next, goal)
                frontier.put((priority, next))
                came_from[next] = current

    # Reconstruct the path
    current = goal
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    return path, iterations  # Return the path and number of iterations

# Function to measure the performance of the search algorithms
def measure_performance(algorithm, map_data, start, goal):
    start_time = time.time()
    path, iterations = algorithm(map_data, start, goal)  # Capture both path and iterations
    elapsed_time = time.time() - start_time
    print(f"Time taken: {elapsed_time:.4f} seconds")
    print(f"Path length: {len(path)} steps")
    print(f"Iterations: {iterations}")
    print("Path:", path)

# Load map from a file
def load_map(filename):
    folder = r"E:\skool\tehisintellekt"
    file_path = os.path.join(folder, filename + '.txt')

    with open(file_path) as f:
        return [line.strip() for line in f.readlines() if len(line) > 1]

# Small maps (hardcoded)
lava_map1 = [
    "      **               **      ",
    "     ***     D        ***      ",
    "     ***                       ",
    "                      *****    ",
    "           ****      ********  ",
    "           ***          *******",
    " **                      ******",
    "*****             ****     *** ",
    "*****              **          ",
    "***                            ",
    "              **         ******",
    "**            ***       *******",
    "***                      ***** ",
    "                               ",
    "                s              ",
]
lava_map2 = [
    "     **********************    ",
    "   *******   D    **********   ",
    "   *******                     ",
    " ****************    **********",
    "***********          ********  ",
    "            *******************",
    " ********    ******************",
    "********                   ****",
    "*****       ************       ",
    "***               *********    ",
    "*      ******      ************",
    "*****************       *******",
    "***      ****            ***** ",
    "                               ",
    "                s              ",
]

# Start and goal positions for small maps
small_map_positions = {
    "lava_map1": ((14, 16), (1, 16)),
    "lava_map2": ((14, 16), (1, 16))
}

# Test with large maps (300x300, 600x600, 900x900)
map_files = {
    "300x300": "cave300x300",
    "600x600": "cave600x600",
    "900x900": "cave900x900"
}

map_starts_goals = {
    "300x300": ((2, 2), (295, 257)),
    "600x600": ((2, 2), (598, 595)),
    "900x900": ((2, 2), (898, 895))
}

# Function to run the search on a selected map
def run_search(map_choice):
    if map_choice == "lava_map1":
        map_data = lava_map1
        start, goal = small_map_positions[map_choice]
    elif map_choice == "lava_map2":
        map_data = lava_map2
        start, goal = small_map_positions[map_choice]
    elif map_choice in map_files:
        # Large maps (300x300, 600x600, 900x900)
        map_data = load_map(map_files[map_choice])
        start, goal = map_starts_goals[map_choice]
    else:
        print(f"Map {map_choice} not found!")
        return

    print(f"\nTesting {map_choice}:")
    
    print("\nBFS:")
    measure_performance(bfs_search, map_data, start, goal)

    print("\nGreedy:")
    measure_performance(greedy_search, map_data, start, goal)

    print("\nA*:") 
    measure_performance(astar_search, map_data, start, goal)

# Main function to select and run search on a map
def main():
    print("Available maps:")
    print("1. lava_map1")
    print("2. lava_map2")
    print("3. 300x300")
    print("4. 600x600")
    print("5. 900x900")
    
    map_choice = input("Enter the map name (e.g., lava_map1, 300x300): ").strip()
    run_search(map_choice)

if __name__ == "__main__":
    main()
