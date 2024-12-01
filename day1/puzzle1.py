
def read_input(file: str) -> list:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    # Parse the lines
    list_1 = []
    list_2 = []

    for line in lines:
        if line.strip() == "":
            continue

        assert "   " in line
        line_split = line.split("   ")
        list_1.append(int(line_split[0]))
        list_2.append(int(line_split[1]))
    
    # Sort the lists
    list_1.sort()
    list_2.sort()
    assert len(list_1) == len(list_2)

    # Build the output
    output = []

    for i in range(len(list_1)):
        output.append((list_1[i], list_2[i]))

    return output

def distance_line(line: list) -> int:
    assert len(line) == 2
    return abs(line[0] - line[1])

list_entries = read_input("input.txt")
total_distance = sum(distance_line(line) for line in list_entries)
print("Total distance between lines is:", total_distance)
