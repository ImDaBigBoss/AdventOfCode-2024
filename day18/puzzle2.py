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

def build_graph(dimensions: tuple) -> dict:
    graph = {}

    for y in range(dimensions[1]):
        for x in range(dimensions[0]):
            graph[(x, y)] = {
                "distance": math.inf,
                "neighbours": []
            }

            for neighbour in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if neighbour[0] < 0 or neighbour[0] >= dimensions[0] or neighbour[1] < 0 or neighbour[1] >= dimensions[1]:
                    continue

                graph[(x, y)]["neighbours"].append(neighbour)

    return graph

def find_lowest_cost(graph: dict, start_position: tuple, end_position: tuple) -> int:
    # Dijkstra's algorithm
    queue = [start_position]
    already_visited = set()

    # Make sure all distances are set to infinity
    for position in graph:
        graph[position]["distance"] = math.inf
    graph[start_position]["distance"] = 0

    while len(queue) > 0:
        queue.sort(key=lambda x: graph[x]["distance"])
        position = queue.pop(0)

        for neighbour_position in graph[position]["neighbours"]:
            neighbour_distance = graph[position]["distance"] + 1

            if neighbour_distance < graph[neighbour_position]["distance"]:
                graph[neighbour_position]["distance"] = neighbour_distance

                if neighbour_position not in already_visited:
                    queue.append(neighbour_position)
                    already_visited.add(neighbour_position)

    return graph[end_position]["distance"]

bytes_to_fall, start_position, end_position, dimensions = read_input("input.txt")
graph = build_graph(dimensions)
for i in range(-1, len(bytes_to_fall)):
    if i % 10 == 0:
        print("Simulating", i + 1, "bytes (" + str(math.trunc((i + 1) / len(bytes_to_fall) * 100)) + "%)")

    if i != -1:
        # Simulate the byte falling: remove from the graph and delete any neighbours
        x, y = bytes_to_fall[i]
        del graph[(x, y)]
        for neighbour in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if neighbour in graph:
                graph[neighbour]["neighbours"].remove((x, y))

    # Calculate the new graph
    lowest_cost = find_lowest_cost(graph, start_position, end_position)
    if lowest_cost == math.inf:
        print("No path found for byte number", i + 1, "at position", bytes_to_fall[i])
        break

print("Done")
