import re

def read_input(file: str) -> str:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    # Build the output
    output = ""

    for line in lines:
        output += line + "\n"

    return output

def get_all_occurences(data: str) -> list:
    output = []

    for occurence in re.findall(r'(mul\(([0-9])+,([0-9])+\))', data):
        output.append(occurence[0])

    return output

def compute_mul(mul: str) -> int:
    assert "mul(" in mul
    assert ")" in mul

    params = mul.split(",")
    num1 = int(params[0][4:])
    num2 = int(params[1][:-1])

    return num1 * num2

data = read_input("input.txt")
occurences = get_all_occurences(data)
total_sum = sum([compute_mul(i) for i in occurences])
print("Total sum is:", total_sum)
