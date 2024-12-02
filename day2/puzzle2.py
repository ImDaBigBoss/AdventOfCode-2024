
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

def calculate_variations(report: list) -> list:
    # Compute all the variations
    variations = []
    for i in range(0, len(report) - 1):
        variations.append(report[i] - report[i + 1])
    
    assert len(variations) == len(report) - 1
    return variations

def check_variation_amplitude(variations: list) -> bool:
    # Check the distances: valid is 1, 2 or 3
    for variation in variations:
        if abs(variation) <= 0 or abs(variation) > 3:
            return False # The report is not safe

    return True

def check_variation_sign(variations: list) -> bool:
    # Make sure that all the signs are the same
    increase = None

    for variation in variations:

        if increase == None:
            increase = variation > 0
        elif increase:
            if variation < 0:
                return False
        else:
            if variation > 0:
                return False

    return True

def is_report_safe(report: list) -> bool:
    # Try without the problem fixer magic
    variations = calculate_variations(report)
    safe = check_variation_sign(variations)
    if safe:
        safe = check_variation_amplitude(variations)
    if safe:
        return True

    # This is horrible, but iterate over every possible other list
    for i in range(len(report)):
        new_report = report.copy()
        new_report.pop(i)

        variations = calculate_variations(new_report)
        safe = check_variation_sign(variations)
        if not safe:
            continue
        safe = check_variation_amplitude(variations)
        if safe:
            return True

    return False

report_collection = read_input("input.txt")
total_safe = sum(1 if is_report_safe(report) else 0 for report in report_collection)
print("Total safe reports:", total_safe, "out of", len(report_collection))
