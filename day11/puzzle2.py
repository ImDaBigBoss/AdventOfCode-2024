import math

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

def prepare_for_iteration(stones: list) -> dict:
    output = {}

    for stone in stones:
        if stone not in output:
            output[stone] = 1
        else:
            output[stone] += 1

    return output

def get_num_len(num: int) -> int:
    return 1 if num == 0 else int(math.log10(num)) + 1

def add_to_output(output: dict, num: int, count: int) -> dict:
    if num not in output:
        output[num] = count
    else:
        output[num] += count

    return output

def stone_iteration(stones: dict) -> list:
    output = {}

    for stone in stones:
        count = stones[stone]

        if stone == 0:
            # Set stones with a value of 0 to 1
            add_to_output(output, 1, count)
        else:
            num_len = get_num_len(stone)

            if num_len % 2 == 0:
                # Split the numbers with an even number of digits in half: 1234 becomes 12, 34
                half_len = num_len // 2

                add_to_output(output, stone // (10 ** half_len), count)
                add_to_output(output, stone % (10 ** half_len), count)
            else:
                add_to_output(output, stone * 2024, count)

    return output

stones = read_input("input.txt")
print("There are initially", len(stones), "stones.")
stones = prepare_for_iteration(stones)
for i in range(75):
    stones = stone_iteration(stones)
total_stones = sum([count for count in stones.values()])
print("After iterating, there are", total_stones, "stones.")
