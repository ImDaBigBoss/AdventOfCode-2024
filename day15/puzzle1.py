
class RobotMap:
    def __init__(self, robot_positon: tuple, map_data: list):
        self.robot_position = robot_positon
        self.map_data = map_data
    
    def __push_box(self, box_position: tuple, move: tuple) -> bool:
        new_box_position = (box_position[0] + move[0], box_position[1] + move[1])

        # Find out what the box would be moving into
        next_tile = self.map_data[new_box_position[1]][new_box_position[0]]
        can_move = True

        if next_tile == 1:
            can_move = False
        elif next_tile == 2:
            can_move = self.__push_box(new_box_position, move)
        
        if can_move:
            self.map_data[box_position[1]][box_position[0]] = 0
            self.map_data[new_box_position[1]][new_box_position[0]] = 2

        return can_move
    
    def make_move(self, move: tuple):
        old_position = self.robot_position
        new_position = (old_position[0] + move[0], old_position[1] + move[1])

        # Find out what the robot would be moving into
        next_tile = self.map_data[new_position[1]][new_position[0]]
        can_move = True

        if next_tile == 1: # Wall
            can_move = False
        elif next_tile == 2: # Box
            can_move = self.__push_box(new_position, move)

        # If the robot can move, update its position
        if can_move:
            self.robot_position = new_position
    
    def debug_print(self):
        output = ""
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                if (x, y) == self.robot_position:
                    output += ROBOT_TILE
                elif self.map_data[y][x] == 0:
                    output += EMPTY_TILE
                elif self.map_data[y][x] == 1:
                    output += WALL_TILE
                elif self.map_data[y][x] == 2:
                    output += BOX_TILE
            output += "\n"
        
        print(output)

    def calculate_gps_sum(self) -> int:
        # Gift Positioning System: sum of each box's position (x + 100y)
        gps_sum = 0

        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                if self.map_data[y][x] == 2:
                    gps_sum += x + 100 * y

        return gps_sum

WALL_TILE = "#"
EMPTY_TILE = "."
BOX_TILE = "O"
ROBOT_TILE = "@"
MOVE_DIRECTIONS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0)
}

def read_input(file: str) -> tuple:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    reading_map = True
    robot_start_position = None
    map_data = []
    move_sequence = []

    for y in range(len(lines)):
        cleaned_line = lines[y].strip()
        if cleaned_line == "":
            reading_map = False
            continue

        if reading_map:
            line = []
            for x in range(len(cleaned_line)):
                c = cleaned_line[x]

                if c == WALL_TILE:
                    line.append(1)
                elif c == EMPTY_TILE:
                    line.append(0)
                elif c == BOX_TILE:
                    line.append(2)
                elif c == ROBOT_TILE:
                    robot_start_position = (x, y)
                    line.append(0)
                else:
                    raise ValueError(f"Unknown character '{c}'")

            map_data.append(line)
        else:
            for c in cleaned_line:
                if c in MOVE_DIRECTIONS:
                    move_sequence.append(MOVE_DIRECTIONS[c])
                else:
                    raise ValueError(f"Unknown character '{c}'")
    
    return RobotMap(robot_start_position, map_data), move_sequence

robot_map, move_sequence = read_input("input.txt")
robot_map.debug_print()
for move in move_sequence:
    robot_map.make_move(move)
robot_map.debug_print()
print("The total GPS sum is:", robot_map.calculate_gps_sum())