total_joltage = 0
cells_turned_on = 12

def max_number_with_x_digits_after_it(parts: list[int], idx: int, x: int) -> tuple[int, int]:
    max_number = 0
    found_idx = -1
    # print(f"Finding max number in parts from index {idx} with {x} digits after it")
    for i in range(idx, len(parts) - x):
        if parts[i] > max_number:
            max_number = parts[i]
            found_idx = i
    return max_number, found_idx

with open('input') as f:
    for line in f:
        if not line:
            raise ValueError("Empty line encountered")
        
        print(f"Processing line: {line.strip()}")

        parts = [int(ch) for ch in line.strip()]

        max_jolts_for_line = 0
        found_idx = 0
        for i in range(cells_turned_on):
            max_digit, found_idx = max_number_with_x_digits_after_it(parts, found_idx, cells_turned_on - i - 1)
            # print(f"Max digit for position {i}: {max_digit} at index {found_idx}")
            max_jolts_for_line += max_digit * (10 ** (cells_turned_on - i - 1))
            found_idx += 1  # Move to the next index for the next search

        print(f"Max joltage for line: {max_jolts_for_line}")

        total_joltage += max_jolts_for_line
print(f"Total joltage: {total_joltage}")
