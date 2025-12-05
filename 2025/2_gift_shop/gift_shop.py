total_of_invalid_ids = 0

with open('input') as f:
    for line in f:
        if not line:
            raise ValueError("Empty line encountered")
        parts = line.strip().split(',')
        for part in parts:
            subparts = part.split('-')
            if len(subparts) != 2:
                raise ValueError(f"Part '{part}' does not split into exactly two subparts")
            num_from  = int(subparts[0])
            num_to = int(subparts[1])
            # print(f"Checking gift IDs from {num_from} to {num_to}")

            # Check each gift ID in the range
            for gift_id in range(num_from, num_to + 1):
                # print(f"Checking gift ID: {gift_id}")
                gift_id_invalid = False
                gift_id_str = str(gift_id)
                for i in range(2, len(gift_id_str) + 1):
                    if len(gift_id_str) % i == 0:
                        part_len = len(gift_id_str) // i
                        parts = []
                        for j in range(i):
                            start = j * part_len
                            end = (j + 1) * part_len
                            parts.append(gift_id_str[start:end])
                        # print(f"  Split into {i} parts: {parts}")
                        if all(p == parts[0] for p in parts):
                            # print(f"Gift ID {gift_id} has {i} equal parts: {parts}")
                            gift_id_invalid = True
                if gift_id_invalid:
                    # print(f"Gift ID {gift_id} is invalid")
                    total_of_invalid_ids += gift_id

print(f"Total of invalid gift IDs: {total_of_invalid_ids}")
