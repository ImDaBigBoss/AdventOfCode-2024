
class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

# --- Program

def read_input(file: str) -> str:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    # Build the output
    output = []

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            continue

        line_out = []

        for char in cleaned_line:
            line_out.append(char)
        
        output.append(line_out)

    return output

def find_next(start: Vector, direction: Vector, data: list, current: str, search: str) -> bool:
    if current == search:
        return True
    
    next_char = search[len(current)]

    x = start.x + direction.x
    y = start.y + direction.y

    if x < 0 or x >= len(data[0]) or y < 0 or y >= len(data):
            return False
        
    char = data[y][x]
    if char == next_char:
        return find_next(Vector(x, y), direction, data, current + char, search)

def find_start(data: list, search: str) -> int:
    if len(search) < 2:
        raise Exception("This code can't work...")

    occurences = 0
    first_letter = search[0]
    second_letter = search[1]

    # Search the whole grid for the first letter
    for start_y in range(len(data)):
        for start_x in range(len(data[0])):
            char = data[start_y][start_x]

            if char == first_letter:
                # First letter found
                # Search all around the first letter for the next
                for diff_y in range(-1, 2):
                    y = start_y + diff_y
                    if y < 0 or y >= len(data):
                        continue

                    for diff_x in range(-1, 2):
                        x = start_x + diff_x

                        if x < 0 or x >= len(data[0]):
                            continue

                        char = data[y][x]
                        if char == second_letter:
                            next_start = Vector(x, y)
                            if find_next(next_start, Vector(diff_x, diff_y), data, search[:2], search):
                                occurences += 1
    
    return occurences

data = read_input("input.txt")
search = "XMAS"
occurences = find_start(data, search)
print("There are", occurences, "occurences of \"" + search + "\"")
