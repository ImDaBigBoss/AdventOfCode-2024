
def read_input(file: str) -> list:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    # Parse the lines
    output = []

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            continue

        assert ": " in line
        assert " " in line

        # Remove the colon
        test_value = cleaned_line.split(": ")
        terms = [int(term) for term in test_value[1].split(" ")]
        test_value = int(test_value[0])

        output.append([test_value, terms])

    return output

def reconcile_equasion(test_value: int, terms: list, current_value: int = 0) -> int:
    """Finds the test value by multiplying or adding the following terms together. If that isn't possible, then it returns 0."""

    if terms == None:
        if current_value == test_value:
            return test_value
        else:
            return 0
    else:
        new_list = None
        if len(terms) != 1:
            new_list = terms[1:]

        if current_value == 0:
            return reconcile_equasion(test_value, new_list, terms[0])
        else:
            sol1 = reconcile_equasion(test_value, new_list, current_value + terms[0])
            sol2 = reconcile_equasion(test_value, new_list, current_value * terms[0])
            sol3 = reconcile_equasion(test_value, new_list, int(str(current_value) + str(terms[0])))

            return max(sol1, sol2, sol3)

data = read_input("input.txt")
test_value_sum = sum([reconcile_equasion(entry[0], entry[1]) for entry in data])
print("The total test value sum is", test_value_sum)
