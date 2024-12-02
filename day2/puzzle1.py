
def read_input(file: str) -> list:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    # Build the output
    output = []

    for line in lines:
        if line.strip() == "":
            continue

        assert " " in line
        line_split = line.split(" ")
        output.append([int(entry) for entry in line_split])

    return output

def is_report_safe(report: list) -> bool:
    # Compute all the variations
    variations = []
    for i in range(0, len(report) - 1):
        variations.append(report[i] - report[i + 1])
    
    assert len(variations) == len(report) - 1

    # Check the distances: valid is 1, 2 or 3
    for variation in variations:
        if abs(variation) <= 0 or abs(variation) > 3:
            return False # The report is not safe

    # Make sure that all the signs are the same
    increase = None
    for varition in variations:
        if increase == None:
            increase = varition > 0
        elif increase:
            if varition < 0:
                return False
        else:
            if varition > 0:
                return False

    # The report should be safe
    return True

report_collection = read_input("input.txt")
total_safe = sum(1 if is_report_safe(report) else 0 for report in report_collection)
print("Total safe reports:", total_safe, "out of", len(report_collection))
