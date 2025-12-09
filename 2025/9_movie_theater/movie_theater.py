import sys
import shapely

from shapely import Polygon

def area(a: list[int], b: list[int]) -> int:
    return (abs(b[0] - a[0]) + 1) * (abs(b[1] - a[1]) + 1)

with open(sys.argv[1], "r") as f:
    coordinates = []
    for line in f:
        x, y = line.strip().split(",")
        coordinates.append([int(x), int(y)])

    # Find all the possible polygons that can be made from two points
    rectangles = []
    for point_a in range(len(coordinates)):
        for point_b in range(len(coordinates)):
            if point_a != point_b:
                this_area = area(coordinates[point_a], coordinates[point_b])
                rectangles.append([this_area, coordinates[point_a], coordinates[point_b]])
    
    # Print the largest area and the two points that make it
    rectangles.sort(key=lambda x: x[0], reverse=True)
    print(f"The two furthest points are {rectangles[0][1]} and {rectangles[0][2]} with an area of {rectangles[0][0]}")

    # Now find the largest of these rectangles which fits inside the polygon
    polygon = Polygon(coordinates)
    for rectangle in rectangles:
        box = shapely.box(rectangle[1][0], rectangle[1][1], rectangle[2][0], rectangle[2][1])
        if shapely.contains(polygon, box):
            print(f"The largest intersecting rectangle is between {rectangle[1]} and {rectangle[2]} with an area of {rectangle[0]}")
            break
