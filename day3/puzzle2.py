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

    for occurence in re.findall(r'(mul\(([0-9])+,([0-9])+\))|(do(n\'t)?\(\))', data):
        if "do()" in occurence:
            output.append("yes")
        elif "don't()" in occurence:
            output.append("no")
        else:
            output.append(occurence[0])

    return output

def compute_mul(mul: str) -> int:
    assert "mul(" in mul
    assert ")" in mul

    params = mul.split(",")
    num1 = int(params[0][4:])
    num2 = int(params[1][:-1])

    return num1 * num2

def calculate_sum(occurences: list) -> int:
    enabled = True
    sum = 0

    for occurence in occurences:
        if occurence == "no":
            enabled = False
        elif occurence == "yes":
            enabled = True
        elif enabled:
            sum += compute_mul(occurence)
    
    return sum

data = read_input("input.txt")
occurences = get_all_occurences(data)
total_sum = calculate_sum(occurences)
print("Total sum is:", total_sum)
