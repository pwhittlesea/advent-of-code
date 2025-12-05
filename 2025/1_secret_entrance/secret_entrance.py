starting_position = 50
number_of_ended_at_zero = 0
number_of_clicks_at_zero = 0

with open('input') as f:
    current_pos = starting_position
    for line in f:
        if not line:
            raise ValueError("Empty line encountered")
        first_char = line[0]
        try:
            rest_of_line = int(line[1:].strip())
        except ValueError:
            raise ValueError(f"Expected integer after '{first_char}', got: '{line[1:].strip()}'")

        if first_char == 'L':
            for _ in range(rest_of_line):
                current_pos += 1

                if current_pos % 100 == 0:
                    number_of_clicks_at_zero += 1
        elif first_char == 'R':
            for _ in range(rest_of_line):
                current_pos -= 1

                if current_pos % 100 == 0:
                    number_of_clicks_at_zero += 1
        else:
            raise ValueError(f"Invalid character '{first_char}' in line: {line}")
        
        current_pos = current_pos % 100

        if current_pos == 0:
            number_of_ended_at_zero += 1
        print(f"Current Position: {current_pos}, Move: {first_char} {rest_of_line}")

print(f"Total number of times position ended at zero: {number_of_ended_at_zero}")
print(f"Total number of clicks at zero: {number_of_clicks_at_zero}")
