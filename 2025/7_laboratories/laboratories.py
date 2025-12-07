import sys

def find_beam_start(input: list[list[str]]) -> tuple[int, int]:
    if "S" in input[0]:
        y = input[0].index("S")
        print(f"Beam starts at: (0, {y})")
        return (1, y)
    raise ValueError("Start of beam 'S' not found in input.")


def calc_timelines(tl_cache: list[list[int]], input: list[list[str]], x: int, y: int) -> int:
    if x != len(input) - 1:
        if input[x + 1][y] == ".":
            return calc_timelines(tl_cache, input, x + 1, y)
        elif input[x + 1][y] == "^":
            # If we already have calculated the number of timelines from this point downwards, return that value
            if not tl_cache[x + 1][y]:
                tl_cache[x + 1][y] = calc_timelines(tl_cache, input, x + 1, y - 1) + calc_timelines(tl_cache, input, x + 1, y + 1)
            return tl_cache[x + 1][y]
        else:
            raise ValueError(f"Unexpected character '{input[x + 1][y]}' at position ({x + 1}, {y})")
    return 1


def calc_splits(input: list[list[str]], x: int, y: int) -> int:
    input[x][y] = "|"
    
    if x != len(input) - 1:
        if input[x + 1][y] == ".":
            return calc_splits(input, x + 1, y)
        elif input[x + 1][y] == "^":
            return calc_splits(input, x + 1, y - 1) + calc_splits(input, x + 1, y + 1) + 1
        elif input[x + 1][y] == "|":
            return 0
        else:
            raise ValueError(f"Unexpected character '{input[x + 1][y]}' at position ({x + 1}, {y})")
    return 0


with open(sys.argv[1], "r") as f:
    # Create an array of characters from the input file
    input = []
    for line in f:
        input.append(list(line.strip()))

    tl_cache = [[None for _ in range(len(input[0]))] for _ in range(len(input))]

    # Find the start of the beam and progress it
    x, y = find_beam_start(input)

    print(f"Total timelines: {calc_timelines(tl_cache, input, x, y)}")
    print(f"Total splits: {calc_splits(input, x, y)}")
