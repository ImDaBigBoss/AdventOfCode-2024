
# Based on my input:

# --- Raw assembly code ---
# Exec bst
# Combo reg A
# Exec bxl
# Lit 1
# Exec cdv
# Combo reg B
# Exec bxl
# Lit 5
# Exec adv
# Combo 3
# Exec bxc
# Lit 4
# Exec out
# Combo reg B
# Exec jnz
# Lit 0
#
# --- Pseudo code ---
# B = A % 8
# B = B ^ 1
# C = A / (2**B)
# B = B ^ 5
# A = A / (2**3)
# B = B ^ C
# out (B % 8)
# if A != 0 go to start

def read_input(file: str) -> list:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            continue

        if cleaned_line.startswith("Register "):
            pass
        elif cleaned_line.startswith("Program: "):
            parts = cleaned_line.split(":")[1].strip().split(",")
            return list(map(int, parts))
        else:
            raise Exception(f"Invalid line: {cleaned_line}")

    return None

def reverse_engineer(program: list, value_a: int = None, index_in_prog: int = None) -> int:
    if index_in_prog == None:
        index_in_prog = len(program) - 1
        value_a = 0

    expected_b = program[index_in_prog]
    value_a = value_a << 3

    # Test solution

    possible_ending_values = [ 0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111 ]
    solutions = []

    for a_end in possible_ending_values:
        test_a = value_a + a_end
        a = test_a

        b = a % 8
        b = b ^ 1
        c = a // (2**b)
        b = b ^ 5
        a = a // (2**3)
        b = b ^ c

        if value_a == 0 and a != 0:
            continue # Skip invalid solutions

        if b % 8 == expected_b:
            solutions.append(test_a)

    # Branch out to find the correct solution
    for solution in solutions:
        if index_in_prog == 0:
            return solution

        result = reverse_engineer(program, solution, index_in_prog - 1)
        if result != None:
            return result

    return None

program = read_input("input.txt")
print(reverse_engineer(program))
