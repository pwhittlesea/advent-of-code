with open("input", "r") as f:
    input = []
    for line in f:
        input.append(line)

    # Calculate problem widths from the last line
    final_line = f"{input[-1].strip('\n')} "
    problem_widths = []
    for i, char in enumerate(final_line):
        if char != ' ':
            problem_widths.append(1)
        else:
            problem_widths[-1] += 1
    
    # print(f"Problem widths: {problem_widths}")
    parsed_input = []
    for line in input:
        line = line.rstrip('\n')
        problem_start = 0
        problems = []
        for width in problem_widths:
            problem = line[problem_start:problem_start + width - 1]
            problems.append(problem)
            problem_start += width
        parsed_input.append(problems)

    parsed_input = [list(row) for row in zip(*parsed_input)]

    total_sum = 0
    for row in parsed_input:
        digits = len(row[0])
        flipped_numbers = ['' for _ in range(digits)]
        for x in range(0, digits):
            for entry in row[:-1]:
                # print(f"Entry: '{entry}' - x: {x} - digit: {entry[x]}")
                flipped_numbers[x] = flipped_numbers[x] + entry[x]

        operator = row[-1].strip()
        row_total = -1
        for entry in flipped_numbers:
            if row_total == -1:
                row_total = int(entry)
            elif '*' == operator:
                row_total = row_total * int(entry)
            elif '+' == operator:
                row_total = row_total + int(entry)
            else:
                raise ValueError(f"Unknown operation: {operator}")
        print(f"Operation: '{operator}' - digits: {digits} - numbers {row[:-1]} - flipped numbers: {flipped_numbers} - total: {row_total}")
        total_sum += row_total
    print(f"Total sum: {total_sum}")
