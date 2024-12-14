
class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
        return self

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

class Robot:
    def __init__(self, position: Vector, velocity: Vector):
        self.position = position
        self.velocity = velocity

def read_input(file: str) -> tuple:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    reading_map_size = True

    robots = []
    area_size = None

    for y in range(len(lines)):
        cleaned_line = lines[y].strip()
        if cleaned_line == "":
            reading_map_size = False
            continue

        if reading_map_size:
            assert "," in cleaned_line
            # x,y
            area_size = tuple(map(int, cleaned_line.split(",")))
        else:
            assert "," in cleaned_line and "=" in cleaned_line
            # p=x,y v=x,y
            parts = cleaned_line.split(" ")
            position = parts[0].split("=")[1].split(",")
            velocity = parts[1].split("=")[1].split(",")

            robots.append(Robot(Vector(int(position[0]), int(position[1])), Vector(int(velocity[0]), int(velocity[1]))))

    return robots, area_size

def run_iteration(robots: list, area_size: tuple):
    for robot in robots:
        # Move the robot
        robot.position.add(robot.velocity)

        # If the robot is out of bounds, wrap it around
        if robot.position.x < 0:
            robot.position.x += area_size[0]
        elif robot.position.x >= area_size[0]:
            robot.position.x -= area_size[0]

        if robot.position.y < 0:
            robot.position.y += area_size[1]
        elif robot.position.y >= area_size[1]:
            robot.position.y -= area_size[1]

def count_quadrants(robots: list, area_size: tuple) -> int:
    quad_width = area_size[0]
    quad_height = area_size[1]

    # Build the map data

    map_data = []
    for y in range(quad_height):
        line = []
        for x in range(quad_width):
            count = 0

            for robot in robots:
                if robot.position.x == x and robot.position.y == y:
                    count += 1
            
            line.append(count)
        
        map_data.append(line)

    # Calculate the quadrant sizes

    if quad_width % 2 != 0:
        quad_width -= 1
    if quad_height % 2 != 0:
        quad_height -= 1
    
    quad_width //= 2
    quad_height //= 2

    # Build the quadrants

    quadrants = []

    for mul_x, mul_y in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        quad_x = quad_width * mul_x
        quad_y = quad_height * mul_y

        if quad_x != 0:
            quad_x += 1
        if quad_y != 0:
            quad_y += 1

        count = 0
        for y in range(quad_height):
            for x in range(quad_width):
                count += map_data[quad_y + y][quad_x + x]
        
        quadrants.append(count)
    
    return quadrants

def print_robots(robots: list, area_size: tuple):
    output = ""

    for y in range(area_size[1]):
        for x in range(area_size[0]):
            count = 0

            for robot in robots:
                if robot.position.x == x and robot.position.y == y:
                    count += 1

            if count == 0:
                output += "."
            else:
                output += str(count)

        output += "\n"

    print(output)

robots, area_size = read_input("input.txt")

#print_robots(robots, area_size)
for i in range(100):
    run_iteration(robots, area_size)
#print_robots(robots, area_size)

quadrant_counts = count_quadrants(robots, area_size)

safety_factor = 1
for count in quadrant_counts:
    safety_factor *= count

print("The safety factor is", safety_factor)