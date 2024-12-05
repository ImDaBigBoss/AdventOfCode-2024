
def read_input(file: str) -> tuple:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    # Build the output
    first_section = True
    priority_list = {}
    updates = []

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            first_section = False
            continue

        if first_section:
            assert "|" in cleaned_line
            x = int(cleaned_line.split("|")[0])
            y = int(cleaned_line.split("|")[1])

            if x in priority_list:
                priority_list[x].append(y)
            else:
                priority_list[x] = [y]
        else:
            assert "," in cleaned_line
            pages = cleaned_line.split(",")
            update = []

            for page in pages:
                update.append(int(page))

            updates.append(update)

    return priority_list, updates

def update_check_rule(update: list, first: int, after: list) -> bool:
    for page in update:
        if page == first:
            break
        
        if page in after:
            return False

    return True

def validate_update(update: list, rules: dict) -> bool:
    for rule in rules:
        if rule not in update:
            continue

        if not update_check_rule(update, rule, rules[rule]):
            return False

    return True

def get_update_middle(update: list) -> int:
    if len(update) % 2 == 0:
        raise Exception("Unsure what to do here")

    return update[len(update) // 2]

def get_valid_middle_sum(rules: dict, updates: list) -> int:
    total = 0

    for update in updates:
        if validate_update(update, rules):
            total += get_update_middle(update)

    return total

priority_list, updates = read_input("input.txt")
print("The sum of the valid middle pages is", get_valid_middle_sum(priority_list, updates))