
def read_input(file: str) -> list:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    plot_data = []

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            continue

        plot_data.append(cleaned_line)

    return plot_data

def build_group_data(plot_data: list) -> tuple:
    # Number each tile in the plot
    group_map = [[x + y*len(plot_data[0]) for x in range(len(plot_data[0]))] for y in range(len(plot_data))]
    adjacent_map = [[0 for x in range(len(plot_data[0]))] for y in range(len(plot_data))]

    # Group the tiles:
    # - If an adjacent tile has the same value in the plot_data, they can be grouped together
    # - An adjacent tile is up, down, left, or right of the current tile; not diagonal
    # Merging groups:
    # - All the tiles with the old group id are updated to the new group id
    # - A new perimeter is calculated

    for y in range(len(plot_data)):
        for x in range(len(plot_data[y])):
            current_id = group_map[y][x]
            current_value = plot_data[y][x]

            groups_to_merge = []

            # Check around the current tile
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                new_x = x + dx
                new_y = y + dy

                if new_x < 0 or new_x >= len(plot_data[y]) or new_y < 0 or new_y >= len(plot_data):
                    continue

                test_id = group_map[new_y][new_x]
                test_value = plot_data[new_y][new_x]

                if test_value == current_value:
                    adjacent_map[y][x] += 1
                    if test_id not in groups_to_merge:
                        groups_to_merge.append(test_id)

            # Merge the groups
            for group_id in groups_to_merge:
                # Update the group id for all the tiles
                for tmp_y in range(len(plot_data)):
                    for tmp_x in range(len(plot_data[tmp_y])):
                        if group_map[tmp_y][tmp_x] == group_id:
                            group_map[tmp_y][tmp_x] = current_id

    # Calculate the perimeter and area for each group
    group_data = {}

    for y in range(len(plot_data)):
        for x in range(len(plot_data[y])):
            group_id = group_map[y][x]
            if group_id not in group_data:
                group_data[group_id] = [0, 0]

            group_data[group_id][0] += 4 - adjacent_map[y][x] # Perimeter
            group_data[group_id][1] += 1 # Area

    return group_data

def calculate_price(group_data: dict) -> int:
    total_price = 0

    # Calculate the price of each group
    for group_id in group_data:
        group = group_data[group_id]
        price = group[0] * group[1] # Perimeter * Area
        total_price += price

    return total_price

plot_data = read_input("input.txt")
group_data = build_group_data(plot_data)
total_price = calculate_price(group_data)
print("The total price is", total_price)