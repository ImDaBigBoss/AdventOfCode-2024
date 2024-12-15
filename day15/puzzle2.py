
class RobotMap:
    def __init__(self, robot_positon: tuple, map_data: list):
        self.robot_position = robot_positon
        self.map_data = map_data
    
    def __push_box(self, box_position: tuple, move: tuple, do_motion: bool = True) -> bool:
        assert (move[0] == 0 and move[1] != 0) or (move[0] != 0 and move[1] == 0), "Invalid move"
        assert self.map_data[box_position[1]][box_position[0]] == 2 or self.map_data[box_position[1]][box_position[0]] == 3, "Invalid box tile"

        # Make sure we have the left most tile
        if self.map_data[box_position[1]][box_position[0]] == 3:
            box_position = (box_position[0] - 1, box_position[1])
        new_box_position = (box_position[0] + move[0], box_position[1] + move[1])

        # Find out what the box would be moving into
        can_move = True

        if move[0] == 0: # Vertical move
            next_left_tile = self.map_data[new_box_position[1]][new_box_position[0]] # Tile after the left tile
            left_can_move = True
            if next_left_tile == 1:
                left_can_move = False
            elif next_left_tile == 2 or next_left_tile == 3:
                left_can_move = self.__push_box(new_box_position, move, False)
            
            next_right_tile = self.map_data[new_box_position[1]][new_box_position[0] + 1] # Tile after the right tile
            right_can_move = True
            if next_right_tile == 1:
                right_can_move = False
            elif next_right_tile == 2: # No need to check for 3, as it's the right most tile, if there's a 3, there's a 2 on the left
                right_can_move = self.__push_box((new_box_position[0] + 1, new_box_position[1]), move, False)

            if not left_can_move or not right_can_move:
                can_move = False

            if can_move and do_motion:
                if next_left_tile == 2 or next_left_tile == 3:
                    self.__push_box(new_box_position, move)
                if next_right_tile == 2:
                    self.__push_box((new_box_position[0] + 1, new_box_position[1]), move)

                self.map_data[box_position[1]][box_position[0]] = 0
                self.map_data[box_position[1]][box_position[0] + 1] = 0
                self.map_data[new_box_position[1]][new_box_position[0]] = 2
                self.map_data[new_box_position[1]][new_box_position[0] + 1] = 3
        else: # Horizontal move
            next_tile = None
            if move[0] == -1:
                next_tile = self.map_data[new_box_position[1]][new_box_position[0]] # Tile after the left tile
            else:
                next_tile = self.map_data[new_box_position[1]][new_box_position[0] + 1] # Tile after the right tile

            if next_tile == 1:
                can_move = False
            elif next_tile == 2 or next_tile == 3:
                if move[0] == -1:
                    can_move = self.__push_box(new_box_position, move)
                else:
                    can_move = self.__push_box((new_box_position[0] + 1, new_box_position[1]), move)

            if can_move:
                self.map_data[box_position[1]][box_position[0]] = 0
                self.map_data[box_position[1]][box_position[0] + 1] = 0
                self.map_data[new_box_position[1]][new_box_position[0]] = 2
                self.map_data[new_box_position[1]][new_box_position[0] + 1] = 3

        return can_move
    
    def make_move(self, move: tuple):
        old_position = self.robot_position
        new_position = (old_position[0] + move[0], old_position[1] + move[1])

        # Find out what the robot would be moving into
        next_tile = self.map_data[new_position[1]][new_position[0]]
        can_move = True

        if next_tile == 1: # Wall
            can_move = False
        elif next_tile == 2 or next_tile == 3: # Box
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
                    output += BOX_LEFT_TILE
                elif self.map_data[y][x] == 3:
                    output += BOX_RIGHT_TILE
            output += "\n"
        
        print(output)

    def calculate_gps_sum(self) -> int:
        # Gift Positioning System: sum of each box's position from its left tile (x + 100y)
        gps_sum = 0

        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                if self.map_data[y][x] == 2: # Box left tile
                    gps_sum += x + 100 * y

        return gps_sum

WALL_TILE = "#"
EMPTY_TILE = "."
BOX_SMALL_TILE = "O"
BOX_LEFT_TILE = "["
BOX_RIGHT_TILE = "]"
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
                    line.append(1)
                elif c == EMPTY_TILE:
                    line.append(0)
                    line.append(0)
                elif c == BOX_SMALL_TILE:
                    line.append(2)
                    line.append(3)
                elif c == ROBOT_TILE:
                    robot_start_position = (x * 2, y)
                    line.append(0)
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