from itertools import permutations

post_office = (0, 2)
waypoints = [
    (1, 3),
    (2, 2),
    (1, 1),
    (4, 2),
    (3, 1),
    (3, 3),
]


def calc_routes(points: list[tuple], post_office: tuple) -> tuple:
    """Calculates shortest possible distance and returns
    all paths of shortest distance, shortest distance and
    a dict of distances between points."""
    edges = {
        (a, b): {
            (x, y): ((a - x) ** 2 + (b - y) ** 2) ** 0.5 for x, y in [post_office] + waypoints
        }
        for a, b in [post_office] + waypoints
    }
    min_dist, min_paths = float("inf"), []

    for path in permutations(points):
        path = (post_office,) + path
        dist = sum((edges[path[i]][path[i + 1]] for i in range(len(path) - 1)))

        if dist < min_dist:
            min_dist = dist
            min_paths = [path]
        elif dist == min_dist:
            min_paths.append(path)
    return min_paths, min_dist, edges


def path_printer(path: tuple, edges: dict) -> None:
    accum_dist = 0
    print('# ' * 25)
    for i in range(len(path) - 1):
        accum_dist += edges[path[i]][path[i + 1]]
        print(f"{path[i]} -> {path[i + 1]}: [{accum_dist}]")
    print(f"Total distance = {accum_dist}\n")


if __name__ == '__main__':
    paths, shortest_distance, edges = calc_routes(waypoints, post_office)
    for path in paths:
        path_printer(path, edges)
