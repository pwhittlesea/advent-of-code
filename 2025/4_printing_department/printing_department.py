roll_of_paper = "@"

max_roll_count = 4

def run(lines: list[list[str]]):
    number_of_accessible_rolls = 0
    new_lines = lines.copy()
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            # check the 8 spaces around lines[i][j]
#             print(f"Checking position ({i}, {j}) length {len(lines[i])}")
            top_left = lines[i-1][j-1] if i > 0 and j > 0 else None
            top = lines[i-1][j] if i > 0 else None
            top_right = lines[i-1][j+1] if i > 0 and j < len(lines[i]) - 1 else None
            left = lines[i][j-1] if j > 0 else None
            right = lines[i][j+1] if j < len(lines[i]) - 1 else None
            bottom_left = lines[i+1][j-1] if i < len(lines) - 1 and j > 0 else None
            bottom = lines[i+1][j] if i < len(lines) - 1 else None
            bottom_right = lines[i+1][j+1] if i < len(lines) - 1 and j < len(lines[i]) - 1 else None
            if lines[i][j] != roll_of_paper:
                continue

            number_of_rolls = 0
            if top_left == roll_of_paper:
                number_of_rolls += 1
            if top == roll_of_paper:
                number_of_rolls += 1
            if top_right == roll_of_paper:
                number_of_rolls += 1
            if left == roll_of_paper:
                number_of_rolls += 1
            if right == roll_of_paper:
                number_of_rolls += 1
            if bottom_left == roll_of_paper:
                number_of_rolls += 1
            if bottom == roll_of_paper:
                number_of_rolls += 1
            if bottom_right == roll_of_paper:
                number_of_rolls += 1
            if (number_of_rolls < max_roll_count):
                number_of_accessible_rolls += 1
                new_lines[i][j] = '.'

#             print(f"Current: {lines[i][j]} -> Top Left: {top_left}, Top: {top}, Top Right: {top_right}, Left: {left}, Right: {right}, Bottom Left: {bottom_left}, Bottom: {bottom}, Bottom Right: {bottom_right}")

    return number_of_accessible_rolls, new_lines

with open("input", "r") as f:
    lines = []
    for line in f:
        # process each line here
        chars = [c for c in line.strip()]
        lines.append(chars)

total_accessible_rolls = 0
while True:
    number_of_accessible_rolls, lines = run(lines)
    total_accessible_rolls += number_of_accessible_rolls
    if number_of_accessible_rolls == 0:
        break
print(total_accessible_rolls)
