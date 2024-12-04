
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

    # The word has to be diagonal
    if direction.x == 0 or direction.y == 0:
        return False

    next_char = search[len(current)]

    x = start.x + direction.x
    y = start.y + direction.y

    if x < 0 or x >= len(data[0]) or y < 0 or y >= len(data):
            return False
        
    char = data[y][x]
    if char == next_char:
        return find_next(Vector(x, y), direction, data, current + char, search)

def find_middle(data: list, search: str) -> list:
    """Returns the centre of each diagonal occurence of the word."""

    if len(search) < 2:
        raise Exception("This code can't work...")
    if len(search) % 2 == 2:
        raise Exception("There is no middle to this word")

    centres = []
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
                            next_direction = Vector(diff_x, diff_y)

                            if find_next(next_start, next_direction, data, search[:2], search):
                                middle = (len(search) // 2)
                                found_centre = Vector(start_x + (middle * diff_x), start_y + (middle * diff_y))
                                centres.append(found_centre)
    
    return centres

def count_pairs(centres: list) -> int:
    # Count the number of times which each value is found
    occurences = {}

    for centre in centres:
        repr = str(centre)
        if repr in occurences:
            occurences[repr] += 1
        else:
            occurences[repr] = 1

    # Count the number of pairs
    total = 0

    for entry in occurences:
        if occurences[entry] == 2:
            total += 1

    return total

data = read_input("input.txt")
search = "MAS"
centres = find_middle(data, search)
pair_count = count_pairs(centres)
print("There are", pair_count, "X-\"" + search + "\"s")
