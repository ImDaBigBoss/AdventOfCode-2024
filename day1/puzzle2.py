
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

    assert len(list_1) == len(list_2)
    return list_1, list_2

def num_occurences(num: int, compare: list) -> int:
    occurences = 0

    for entry in compare:
        if entry == num:
            occurences += 1

    return num * occurences

list_1, list_2 = read_input("input.txt")
score = sum(num_occurences(entry, list_2) for entry in list_1)
print("Similarity score is:", score)
