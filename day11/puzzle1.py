
def read_input(file: str) -> list:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    stones = []

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            continue

        stones.extend([int(c) for c in cleaned_line.split(" ")])

    return stones

def stone_iteration(stones: list) -> list:
    output = []

    for stone in stones:
        if stone == 0:
            # Set stones with a value of 0 to 1
            output.append(1)
        elif len(str(stone)) % 2 == 0:
            # Split the numbers with an even number of digits in half: 1234 becomes 12, 34
            str_stone = str(stone)
            half_len = len(str_stone) // 2

            output.append(int(str_stone[:half_len]))
            output.append(int(str_stone[half_len:]))
        else:
            output.append(stone * 2024)

    return output

stones = read_input("input.txt")
print("There are initially", len(stones), "stones.")
for i in range(25):
    stones = stone_iteration(stones)
print("After iterating, there are", len(stones), "stones.")
