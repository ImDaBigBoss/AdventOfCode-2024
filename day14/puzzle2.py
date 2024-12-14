
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

def test_if_tree(robots: list, area_size: tuple) -> bool:
    # We just need to find a line of 20 in a row on two lines and it should be safe to assume that it's the christmas tree border

    # Test to see if there are 20 on the same y axis
    max_number = 0
    line_count = -1

    for y in range(area_size[1]):
        count = 0

        for robot in robots:
            if robot.position.y == y:
                count += 1

        if count > max_number:
            max_number = count
            line_count = y
    
    if max_number < 20:
        return False
    
    # Now find out if they have a continuous x axis

    row_started = False
    row_count = 0

    for x in range(area_size[0]):
        count = 0

        for robot in robots:
            if robot.position.y == line_count and robot.position.x == x:
                count += 1
        
        if count > 0:
            row_count += 1
            row_started = True
        else:
            if row_started:
                break

    return row_count >= 20

def print_robots(robots: list, area_size: tuple):
    output = ""

    for y in range(area_size[1]):
        for x in range(area_size[0]):
            count = 0

            for robot in robots:
                if robot.position.x == x and robot.position.y == y:
                    count += 1

            if count == 0:
                output += " "
            else:
                output += "#"

        output += "\n"

    print(output)

robots, area_size = read_input("input.txt")
print("Searching...")

for i in range(1000000):
    run_iteration(robots, area_size)
    if test_if_tree(robots, area_size):
        print_robots(robots, area_size)
        print("The tree was found after", i + 1, "iterations")
        break
    elif i % 100 == 0:
        print("Iteration", i + 1, "done")
