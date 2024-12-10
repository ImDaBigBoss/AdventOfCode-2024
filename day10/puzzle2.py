
class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def copy(self):
        return Vector(self.x, self.y)

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

def read_input(file: str) -> list:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    map_data = []

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            continue

        map_data.append([int(c) for c in cleaned_line])

    return map_data

def find_starting_points(map_data: list) -> list:
    starting_points = []

    for y in range(len(map_data)):
        for x in range(len(map_data[y])):
            if map_data[y][x] == 0:
                starting_points.append(Vector(x, y))

    return starting_points

def find_next_point(map_data: list, current_position: Vector, current_value: int) -> int:
    assert map_data[current_position.y][current_position.x] == current_value

    if current_value == 9:
        return [current_position]

    valid_points = []

    for x in range(-1, 2):
        for y in range(-1, 2):
            if (x == 0 and y == 0) or (x != 0 and y != 0):
                continue

            new_position = current_position.copy()
            new_position.add(Vector(x, y))

            if new_position.x < 0 or new_position.x >= len(map_data[0]) or new_position.y < 0 or new_position.y >= len(map_data):
                continue

            if map_data[new_position.y][new_position.x] == current_value + 1:
                valid_points.extend(find_next_point(map_data, new_position, current_value + 1))

    return valid_points

def score_tailheads(map_data: list, starting_points: list) -> list:
    tailheads = []

    for starting_point in starting_points:
        valid_ends = find_next_point(map_data, starting_point, 0)
        tailheads.append(len(valid_ends))

    return tailheads

map_data = read_input("input.txt")
scores = score_tailheads(map_data, find_starting_points(map_data))
total_score = sum(scores)
print("Total revised tailhead score is", total_score)
