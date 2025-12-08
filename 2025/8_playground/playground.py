import sys

def euclidean_distance(point1, point2) -> float:
    return (((point1[1] - point2[1]) ** 2) + ((point1[2] - point2[2]) ** 2) + ((point1[3] - point2[3]) ** 2)) ** 0.5


with open(sys.argv[1], "r") as f:
    max_conns = int(sys.argv[2]) if len(sys.argv) > 2 else sys.maxsize

    # Create an array of box locations from the input file
    box_locations = []
    for idx, line in enumerate(f):
        x, y, z = line.strip().split(',')
        box_locations.append((idx, float(x), float(y), float(z)))

    print(f"Total boxes loaded: {len(box_locations)}")

    distances = []
    for i in range(len(box_locations)):
        for j in range(len(box_locations)):
            if i != j:
                distance = euclidean_distance(box_locations[i], box_locations[j])
                distances.append((box_locations[i], box_locations[j], distance))
    print(f"Total distances calculated: {len(distances)}")

    # Remove duplicate distances (i.e., (A,B) and (B,A) are considered the same)
    unique_distances = {}
    for box1, box2, dist in distances:
        key = tuple(sorted([box1[0], box2[0]]))
        if key not in unique_distances:
            unique_distances[key] = (box1, box2, dist)
    distances = list(unique_distances.values())
    print(f"Total unique distances: {len(distances)}")

    distances.sort(key=lambda x: x[2])
    print("Distances sorted from smallest to largest.")

    box_connections = distances if max_conns >= len(distances) else distances[:max_conns]
    print(f"Total connections made: {len(box_connections)}")

    # Initialize circuits with each box in its own circuit
    circuits = [[idx] for idx in range(len(box_locations))]

    for connection in box_connections:
        from_circuit_idx = None
        to_circuit_idx = None
        for idx, circuit in enumerate(circuits):
            if connection[0][0] in circuit:
                from_circuit_idx = idx
            if connection[1][0] in circuit:
                to_circuit_idx = idx

        # Merge circuits if they are different
        if from_circuit_idx != to_circuit_idx:
            circuits[from_circuit_idx].extend(circuits[to_circuit_idx])
            del circuits[to_circuit_idx]

        if len(circuits) == 1:
            print(f"All boxes are connected in a single circuit by connection: {connection}")
            print(f"{int(connection[0][1] * connection[1][1])}")
            break

    if len(circuits) > 1:
        circuits.sort(key=lambda c: len(c), reverse=True)
        if len(circuits) >= 3:
            one = len(circuits[0])
            two = len(circuits[1])
            three = len(circuits[2])
            result = one * two * three
            print(f"Product of the largest 3 circuits ({one}, {two}, {three}) sizes: {result}")
        else:
            print("Not enough circuits to multiply the largest 3 sizes.")
