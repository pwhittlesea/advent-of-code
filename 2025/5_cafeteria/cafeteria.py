with open("input", "r") as f:
    total_fresh = 0
    range_pairs = []
    ingredients = []
    mode = "r"
    total_fresh_possible_ingredients = 0

    for line in f:
        if line.strip() == "":
            mode = "i"
            continue

        if mode == "r":
            # here we read ranges
            start, end = line.strip().split('-')
            print(f"Reading range line: {start}-{end}")
            range_pairs.append([int(start), int(end)])
        if mode == "i":
            # here we read ingredients
            print(f"Reading ingredient line: {line.strip()}")
            ingredients.append(int(line.strip()))

    range_pairs.sort(key=lambda x: x[0])

    for ingredient in ingredients:
        for start, end in range_pairs:
            if ingredient >= start and ingredient <= end:
                total_fresh += 1
                break

    merged_pairs = []
    for start, end in range_pairs:
        if not merged_pairs or start > merged_pairs[-1][1]:
            merged_pairs.append([start, end])
        else:
            merged_pairs[-1][1] = max(merged_pairs[-1][1], end)

    total_fresh_possible_ingredients = sum([end - start + 1 for start, end in merged_pairs])

    print("----")
    print(f"Total fresh ingredients: {total_fresh}")
    print(f"Total fresh possible ingredients so far: {total_fresh_possible_ingredients}")
