import math

WALL_TILE = "#"
EMPTY_TILE = "."
START_POSITION = "S"
END_POSITION = "E"

START_DIRECTION = (1, 0)

def read_input(file: str) -> tuple:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    map_data = []
    start_position = None
    end_position = None

    for y in range(len(lines)):
        cleaned_line = lines[y].strip()
        if cleaned_line == "":
            continue

        line = []
        for x in range(len(cleaned_line)):
            c = cleaned_line[x]

            if c == WALL_TILE:
                line.append(1)
            elif c == EMPTY_TILE:
                line.append(0)
            elif c == START_POSITION:
                start_position = (x, y)
                line.append(0)
            elif c == END_POSITION:
                end_position = (x, y)
                line.append(0)
            else:
                raise ValueError(f"Unknown character '{c}'")

        map_data.append(line)

    assert start_position is not None, "Start position not found"
    assert end_position is not None, "End position not found"

    return map_data, start_position, end_position

def calculate_graph(map_data: list, start_position: tuple) -> dict:
    graph = {}

    # Build a graph where each node is a fork in the path, the distance for each node is infinity.
    # neighbours are the nodes that can be reached from the current node, they all have a weight
    # which is equal to the number of pixels to move to the next node (has to be a straight line)

    queue = []
    already_queued = set()

    def add_to_queue(position: tuple, direction: tuple):
        entry = (position, direction)
        if entry in already_queued:
            return

        already_queued.add(entry)
        queue.append(entry)

    def search_branch(position: tuple, direction: tuple):
        # Create the start node if it does not exist
        if position not in graph:
            graph[position] = {
                "distance": math.inf,
                "turn_weight": 0,
                "neighbours": {}
            }

        x, y = position

        # Calculate the distance to the next node
        times_moved = 0
        available_directions = []

        while True:
            available_directions.clear()

            # Find all available directions
            for dir_x, dir_y in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                tmp_x = x + dir_x
                tmp_y = y + dir_y

                # If leaves map
                if tmp_x < 0 or tmp_y < 0 or tmp_x >= len(map_data[0]) or tmp_y >= len(map_data):
                    continue

                # If this is backtracking, ignore it
                if dir_x == -direction[0] and dir_y == -direction[1]:
                    continue

                # If there is an open path in the direction, add it to the available directions
                if map_data[tmp_y][tmp_x] == 0:
                    available_directions.append((dir_x, dir_y))

            if x == position[0] and y == position[1]:
                # If we are at the start position, we can only go in the direction we came from
                if direction not in available_directions:
                    break
            elif direction not in available_directions or len(available_directions) != 1:
                break

            x += direction[0]
            y += direction[1]
            times_moved += 1

        if (x != position[0] or y != position[1]) and times_moved != 0:
            # Create the end node if it does not exist
            if (x, y) not in graph:
                graph[(x, y)] = {
                    "distance": math.inf,
                    "turn_weight": 0,
                    "neighbours": {}
                }

            # Record the branch
            graph[position]["neighbours"][direction] = {
                "position": (x, y),
                "weight": times_moved
            }
            graph[(x, y)]["neighbours"][(-direction[0], -direction[1])] = {
                "position": position,
                "weight": times_moved
            }

        # Search for the next branch
        for dir in available_directions:
            # Ignore going back on the same path
            if dir in graph[(x, y)]["neighbours"]:
                continue

            if dir == direction and (x, y) == position:
                raise ValueError("Invalid recursion detected")

            add_to_queue((x, y), dir)

    for dir in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        add_to_queue(start_position, dir)

    while len(queue) > 0:
        position, direction = queue.pop(0)
        search_branch(position, direction)

    return graph

def debug_graph_to_map(graph: dict, map_data: list, end_position: tuple = None):
    width = len(map_data[0])
    height = len(map_data)

    output = [["#" for _ in range(width)] for _ in range(height)]

    for position, node in graph.items():
        x, y = position
        output[y][x] = "."

        for direction, neighbor in node["neighbours"].items():
            for i in range(neighbor["weight"]):
                output[y + i * direction[1]][x + i * direction[0]] = "."

    if end_position is not None:
        # Draw the path, going from start to end via the shortest path
        current_position = end_position
        current_direction = None
        # Go back to the start position
        while current_position != None:
            print(graph[current_position])

            x, y = current_position
            smallest_distance = math.inf

            if current_direction == (1, 0):
                output[y][x] = "<"
            elif current_direction == (0, 1):
                output[y][x] = "^"
            elif current_direction == (-1, 0):
                output[y][x] = ">"
            elif current_direction == (0, -1):
                output[y][x] = "v"
            else:
                output[y][x] = "X"

            for direction, neighbor in graph[current_position]["neighbours"].items():
                dist = graph[neighbor["position"]]["distance"]
                if dist == 0:
                    output[neighbor["position"][1]][neighbor["position"][0]] = "X"
                    current_position = None
                    break
                elif dist < smallest_distance:
                    smallest_distance = dist
                    current_position = neighbor["position"]
                    current_direction = direction

    text_out = "Graph:\n"
    text_out += "\n".join(["".join([str(c) for c in line]) for line in output])

    print(text_out)

def compute_number_turns(direction: tuple, new_direction: tuple) -> int:
    if direction == new_direction:
        return 0

    if direction[0] == -new_direction[0] and direction[1] == -new_direction[1]:
        return 2

    return 1

assert compute_number_turns((1, 0), (0, 1)) == 1
assert compute_number_turns((1, 0), (0, -1)) == 1
assert compute_number_turns((1, 0), (1, 0)) == 0
assert compute_number_turns((1, 0), (-1, 0)) == 2

def find_lowest_cost(graph: dict, start_position: tuple, end_position: tuple) -> int:
    # Return the cost of the shortest path from start_position to end_position, it is the sum of:
    # - 1x the weight of the edge between the nodes
    # - 1000x the number of turns made by 90 degrees (clockwise or counterclockwise)

    # Initialize the distance to the start position to 0
    graph[start_position]["distance"] = 0

    # Initialize the queue with the start position and the initial direction (facing East)
    queue = [(0, start_position, START_DIRECTION)]
    already_visited = set()

    def dequeue():
        best = math.inf
        best_index = -1

        for i in range(len(queue)):
            value = queue[i][0]

            if value < best:
                best = value
                best_index = i

        return queue.pop(best_index)[1:]

    def enqueue(new_distance, new_position, new_direction):
        queue.append((new_distance, new_position, new_direction))

    while queue:
        # Pull the node with the smallest distance from the queue by sorting it based on the distance
        current_position, current_direction = dequeue()
        current_node = graph[current_position]

        # Check if the current node is the end node
        if current_position == end_position:
            return current_node["distance"]
    
        # Check if the current node has already been visited
        if (current_position, current_direction) in already_visited:
            continue

        already_visited.add((current_position, current_direction))

        # Update the distance of the neighbours
        for direction, neighbor in current_node["neighbours"].items():
            neighbor_position = neighbor["position"]
            neighbor_node = graph[neighbor_position]
            new_distance = current_node["distance"] + neighbor["weight"]

            # Add the turn bias
            new_distance += compute_number_turns(current_direction, direction) * 1000

            if new_distance < neighbor_node["distance"]:
                neighbor_node["distance"] = new_distance
                enqueue(new_distance, neighbor_position, direction)

    return -1

map_data, start_position, end_position = read_input("input.txt")
graph = calculate_graph(map_data, start_position)
assert start_position in graph and end_position in graph, "Start or end position not in graph"
cost = find_lowest_cost(graph, start_position, end_position)
debug_graph_to_map(graph, map_data, end_position)
print("Found a cost of", cost)
