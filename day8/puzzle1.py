
class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
        return self
    
    def mul(self, scalar: int):
        self.x *= scalar
        self.y *= scalar
        return self

    def diff(self, vector):
        return Vector(vector.x - self.x, vector.y - self.y)

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

# --- Program

BLANK_SPOT_CHAR = "."

def read_input(file: str) -> list:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    map_data = []

    for y in range(len(lines)):
        cleaned_line = lines[y].strip()
        if cleaned_line == "":
            continue

        line = []

        for x in range(len(cleaned_line)):
            c = cleaned_line[x]
            line.append(c)

        map_data.append(line)

    return map_data

def get_antenna_freq_positions(map_data: list) -> dict:
    output = {}

    for y in range(len(map_data)):
        for x in range(len(map_data[y])):
            frequency = map_data[y][x]
            if frequency == BLANK_SPOT_CHAR:
                continue

            location = Vector(x, y)

            if frequency in output:
                output[frequency].append(location)
            else:
                output[frequency] = [location]
    
    return output

def calculate_antinode_positions(width: int, height: int, antenna_freq_positions: dict) -> list:
    output = []

    # Loop over each frequency seperately
    for frequency in antenna_freq_positions:
        antenna_positions = antenna_freq_positions[frequency]

        # Loop over each antenna within the frequency
        for position in antenna_positions:
            other_positions = antenna_positions.copy()
            other_positions.remove(position)

            # Loop over every OTHER antenna
            for other_position in other_positions:
                # Calculate the relative antinode position
                antinode = position.diff(other_position).mul(2)
                # Convert to absolute position
                antinode.add(position)

                # Ignore positions outside the map
                if antinode.x < 0 or antinode.y < 0 or antinode.x >= width or antinode.y >= height:
                    continue

                if antinode not in output:
                    output.append(antinode)

    return output

def debug_print_map(width: int, height: int, antenna_freq_positions: dict, antinodes: list):
    for y in range(height):
        line = ""
        for x in range(width):
            current_pos = Vector(x, y)
            found_freq = None

            for freq in antenna_freq_positions:
                if current_pos in antenna_freq_positions[freq]:
                    found_freq = freq
                    break

            if found_freq != None:
                line += found_freq
            elif current_pos in antinodes:
                line += "#"
            else:
                line += "."

        print(line)

    print("")

map_data = read_input("input.txt")
width = len(map_data[0])
height = len(map_data)

antenna_freq_positions = get_antenna_freq_positions(map_data)
antonode_positions = calculate_antinode_positions(width, height, antenna_freq_positions)
#debug_print_map(width, height, antenna_freq_positions, antonode_positions)
print("There are", len(antonode_positions), "antinode positions.")