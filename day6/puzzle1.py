
class Guard:
    def __init__(self, x: int, y: int, direction: int):
        self.x = x
        self.y = y
        self.direction = direction
    
    def move(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_current_pos(self) -> tuple:
        return self.x, self.y

    def calculate_next(self) -> tuple:
        if self.direction == 0: # UP
            return self.x, self.y-1
        elif self.direction == 1: # RIGHT
            return self.x+1, self.y
        elif self.direction == 2: # DOWN
            return self.x, self.y+1
        else: # LEFT
            return self.x-1, self.y

    def rotate_right(self):
        self.direction = (self.direction + 1) % 4
    
    def copy(self):
        return Guard(self.x, self.y, self.direction)
    
    def __repr__(self):
        return "Guard[" + str(self.x) + "," + str(self.y) + "->" + str(self.direction) + "]"

WALL_VALUE = "#"
GUARD_DIRECTIONS = [ "^", ">", "<", "v" ]

# --- Program

def read_input(file: str) -> tuple:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    table = []
    guard_pos = None
    guard_dir = -1

    for y in range(len(lines)):
        cleaned_line = lines[y].strip()
        if cleaned_line == "":
            continue

        line = []

        for x in range(len(cleaned_line)):
            c = cleaned_line[x]

            if c == WALL_VALUE:
                line.append(1)
            else:
                line.append(0)
                if c in GUARD_DIRECTIONS:
                    guard_dir = GUARD_DIRECTIONS.index(c)
                    guard_pos = [x, y]

        table.append(line)

    return table, Guard(guard_pos[0], guard_pos[1], guard_dir)

def debug_print_map(map_data: list) -> str:
    output = ""

    for line in map_data:
        for entry in line:
            if entry == 1:
                output += "#"
            elif entry == 2:
                output += "X"
            else:
                output += "."
        output += "\n"
    
    print(output)

def is_invalid_move(map_data: list, x: int, y: int) -> bool:
    return x < 0 or y < 0 or x >= len(map_data[0]) or y >= len(map_data)

def simulate_guard(map_data: list, guard: Guard):
    guard = guard.copy()

    valid_move = True

    while valid_move:
        x, y = guard.calculate_next()
        if is_invalid_move(map_data, x, y):
            valid_move = False

        if valid_move and map_data[y][x] == 1:
            guard.rotate_right()
        else:
            old_x, old_y = guard.get_current_pos()
            map_data[old_y][old_x] = 2
            guard.move(x, y)
            #debug_print_map(map_data)

def map_count_positions(map_data: list) -> int:
    total = 0

    for line in map_data:
        for entry in line:
            if entry == 2:
                total += 1

    return total

map_data, guard = read_input("input.txt")
simulate_guard(map_data, guard)
total_valid = map_count_positions(map_data)
print("There are", total_valid, "total valid positions on the map!")
