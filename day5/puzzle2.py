import math

def find_min(list: list) -> int:
    min = math.inf

    for value in list:
        if value < min:
            min = value

    return min

# --- Program

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

def correct_update_order(update: list, rules: dict):
    for rule in rules:
        if rule not in update:
            continue
        if update_check_rule(update, rule, rules[rule]):
            continue

        after = [i for i in rules[rule] if i in update]
        if len(after) == 0:
            continue

        update.remove(rule)

        after_indecies = [update.index(i) for i in after]
        min_after = find_min(after_indecies)

        update.insert(min_after, rule)

    return True

def get_corrected_invalid_middle_sum(rules: dict, updates: list) -> int:
    total = 0

    for update in updates:
        if not validate_update(update, rules):
            correct_update_order(update, rules)

            assert validate_update(update, rules)
            total += get_update_middle(update)

    return total

priority_list, updates = read_input("input.txt")
print("The sum of the corrected invalid middle pages is", get_corrected_invalid_middle_sum(priority_list, updates))