
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

def list_deep_copy(list: list) -> list:
    out = []
    for line in list:
        out.append(line.copy())
    return out

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
            elif entry == 3:
                output += "O"
            else:
                output += "."
        output += "\n"
    
    print(output)

def is_invalid_move(map_data: list, x: int, y: int) -> bool:
    return x < 0 or y < 0 or x >= len(map_data[0]) or y >= len(map_data)

def simulate_guard(map_data: list, guard: Guard) -> bool:
    """Returns if the guard is stuck in a loop"""

    guard = guard.copy()

    valid_move = True
    turn_positions = []
    just_turned = False

    while valid_move:
        x, y = guard.calculate_next()
        if is_invalid_move(map_data, x, y):
            valid_move = False

        if valid_move and (map_data[y][x] == 1 or map_data[y][x] == 3):
            # Check if the guard is stuck in a loop
            if not just_turned:
                x, y = guard.get_current_pos()
                turn_position_str = str(x) + "," + str(y)
                if turn_position_str in turn_positions:
                    return True
                else:
                    turn_positions.append(turn_position_str)

            guard.rotate_right()
            just_turned = True
        else:
            just_turned = False
            old_x, old_y = guard.get_current_pos()
            map_data[old_y][old_x] = 2
            guard.move(x, y)
            #debug_print_map(map_data)

    return False

def count_map_loop_paths(map_data: list) -> int:
    total = 0

    if simulate_guard(list_deep_copy(map_data), guard):
        total += 1

    for y in range(len(map_data)):
        for x in range(len(map_data[y])):
            if map_data[y][x] != 0:
                continue

            new_map = list_deep_copy(map_data)
            new_map[y][x] = 3

            got_stuck = simulate_guard(new_map, guard)
            if got_stuck:
                #debug_print_map(new_map)
                total += 1

    return total

map_data, guard = read_input("input.txt")
total_loop = count_map_loop_paths(map_data)
print("There are", total_loop, "total loop creating scenarios on the map!")
