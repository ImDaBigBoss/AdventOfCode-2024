
def read_input(file: str) -> list:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    filesystem = ""

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            continue

        filesystem = cleaned_line
        break

    return filesystem

def process_raw_data(filesystem: str) -> list:
    output = []

    empty_space = False
    block_id = 0

    for c in filesystem:
        if empty_space:
            output.extend([ -1 ] * int(c))
        else:
            output.extend([ block_id ] * int(c))
            block_id += 1

        empty_space = not empty_space
    
    return output

def is_minimised(filesystem: list) -> bool:
    """Returns if there are any empty blocks in the middle of the data."""

    found_empty = False
    for id in filesystem:
        if found_empty and id != -1:
            return False
        if id == -1:
            found_empty = True

    return True

def find_first_occurence(filesystem: list, id: int) -> int:
    for offset in range(len(filesystem)):
        if filesystem[offset] == -1:
            return offset

    return -1

def minimise_fs(filesystem: list):
    while not is_minimised(filesystem):
        destination = find_first_occurence(filesystem, -1)
        filesystem[destination] = filesystem.pop()

def compute_checksum(filesystem: list) -> int:
    checksum = 0

    for offset in range(len(filesystem)):
        id = filesystem[offset]
        if id == -1:
            break

        checksum += id * offset
    
    return checksum

filesystem = read_input("input.txt")
processed_fs = process_raw_data(filesystem)
minimise_fs(processed_fs)
checksum = compute_checksum(processed_fs)
print("Found checksum", checksum)
