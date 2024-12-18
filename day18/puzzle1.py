import math

def read_input(file: str) -> tuple:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    bytes_to_fall = []
    reading_bytes = True
    start_position = None
    end_position = None
    dimensions = None

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            reading_bytes = False
            continue

        if reading_bytes:
            assert "," in cleaned_line

            x, y = cleaned_line.split(",")
            bytes_to_fall.append((int(x), int(y)))
        else:
            assert "w=" in cleaned_line and "h=" in cleaned_line

            w, h = cleaned_line.split(",")
            dimensions = (int(w.split("=")[1]), int(h.split("=")[1]))
            start_position = (0, 0)
            end_position = (dimensions[0] - 1, dimensions[1] - 1)

    assert start_position is not None, "Start position not found"
    assert end_position is not None, "End position not found"
    assert dimensions is not None, "Dimensions not found"

    return bytes_to_fall, start_position, end_position, dimensions

SAFE_TILE = "."
UNSAFE_TILE = "#"

def debug_print_map(corrupted_positions: list, dimensions: tuple):
    output = ""

    for i in range(dimensions[1]):
        for j in range(dimensions[0]):
            if (j, i) in corrupted_positions:
                output += UNSAFE_TILE
            else:
                output += SAFE_TILE
        output += "\n"
    
    print(output)

def simulate_n_bytes_fall(bytes_to_fall: list, number: int) -> list:
    return bytes_to_fall[:number]

def calculate_graph(corrupted_positions: list, start_position: tuple, dimensions: tuple) -> dict:
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
                "neighbours": {}
            }
        
        x, y = position

        # Calculate the distance to the next node
        distance = 0
        available_directions = []

        while True:
            available_directions.clear()

            # Find all available directions
            for dir_x, dir_y in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                tmp_x = x + dir_x
                tmp_y = y + dir_y

                # If leaves map
                if tmp_x < 0 or tmp_y < 0 or tmp_x >= dimensions[0] or tmp_y >= dimensions[1]:
                    continue

                # If this is backtracking, ignore it
                if dir_x == -direction[0] and dir_y == -direction[1]:
                    continue

                # If there is an open path in the direction, add it to the available directions
                if (tmp_x, tmp_y) not in corrupted_positions:
                    available_directions.append((dir_x, dir_y))

            if x == position[0] and y == position[1]:
                # If we are at the start position, we can only go in the direction we came from
                if direction not in available_directions:
                    break
            elif direction not in available_directions or len(available_directions) != 1:
                break

            x += direction[0]
            y += direction[1]
            distance += 1
        
        if (x != position[0] or y != position[1]) and distance != 0:
            # Create the end node if it does not exist
            if (x, y) not in graph:
                graph[(x, y)] = {
                    "distance": math.inf,
                    "neighbours": {}
                }
            
            # Record the branch
            graph[position]["neighbours"][direction] = {
                "position": (x, y),
                "weight": distance
            }
            graph[(x, y)]["neighbours"][(-direction[0], -direction[1])] = {
                "position": position,
                "weight": distance
            }
        
        # Search the other branches
        for dir in available_directions:
            # Ignore going back on an already visited path
            if dir in graph[(x, y)]["neighbours"]:
                continue

            if dir == direction and (x, y) == position:
                raise Exception("Infinite loop detected")

            add_to_queue((x, y), dir)

    for dir in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        add_to_queue(start_position, dir)

    while len(queue) > 0:
        position, direction = queue.pop(0)
        search_branch(position, direction)

    return graph

def debug_print_graph(graph: dict, dimensions: tuple):
    output = [[UNSAFE_TILE for _ in range(dimensions[0])] for _ in range(dimensions[1])]

    for position, data in graph.items():
        x, y = position
        output[y][x] = SAFE_TILE

        for direction, neighbour in data["neighbours"].items():
            for i in range(neighbour["weight"]):
                output[y + direction[1] * i][x + direction[0] * i] = SAFE_TILE

    for line in output:
        print("".join(line))

def find_lowest_cost(graph: dict, start_position: tuple, end_position: tuple) -> int:
    # Dijkstra's algorithm
    queue = [start_position]
    already_visited = set()
    graph[start_position]["distance"] = 0

    while len(queue) > 0:
        queue.sort(key=lambda x: graph[x]["distance"])
        position = queue.pop(0)

        for direction, neighbour in graph[position]["neighbours"].items():
            neighbour_position = neighbour["position"]
            neighbour_distance = graph[position]["distance"] + neighbour["weight"]

            if neighbour_distance < graph[neighbour_position]["distance"]:
                graph[neighbour_position]["distance"] = neighbour_distance
                if neighbour_position not in already_visited:
                    queue.append(neighbour_position)
                    already_visited.add(neighbour_position)

    return graph[end_position]["distance"]

bytes_to_fall, start_position, end_position, dimensions = read_input("input.txt")
corrupted_positions = simulate_n_bytes_fall(bytes_to_fall, 1024)
graph = calculate_graph(corrupted_positions, start_position, dimensions)
lowest_cost = find_lowest_cost(graph, start_position, end_position)
print("Found lowest cost:", lowest_cost)
