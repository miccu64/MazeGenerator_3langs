import random


# Hunt and Kill algorithm
# http://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm


# 1 -> lewo, 2 -> prawo, 3 -> dół, 4 -> góra
def number_to_direction(numb: int) -> [int]:
    if numb == 1:
        return [-1, 0]
    if numb == 2:
        return [1, 0]
    if numb == 3:
        return [0, 1]
    if numb == 4:
        return [0, -1]


def opposite_move(numb: int) -> [int]:
    if numb == 1:
        return 2
    if numb == 2:
        return 1
    if numb == 3:
        return 4
    if numb == 4:
        return 3


def random_move(used_moves: [int]) -> int:
    if (len(used_moves)) == 4:
        return 0

    new_direction = 0
    while new_direction == 0 or new_direction in used_moves:
        new_direction = random.randint(1, 4)
    return new_direction


def walk(grid: [], current_x: int, current_y: int, x_grid_size: int, y_grid_size: int) -> [int]:
    used_moves = []
    while len(used_moves) < 4:
        move = random_move(used_moves)
        used_moves.append(move)
        direction = number_to_direction(move)
        new_x = current_x + direction[0]
        new_y = current_y + direction[1]
        if new_x < 0 or new_y < 0 or new_x >= x_grid_size or new_y >= y_grid_size or grid[new_x][new_y] != 0:
            continue
        # grid[new_x][new_y] = move
        grid[current_x][current_y] = move
        return [new_x, new_y]


def hunt(grid: [], x_grid_size: int, y_grid_size: int):
    for x in range(x_grid_size):
        for y in range(y_grid_size):
            if grid[x][y] != 0:
                continue
            neighbors = []

            for move in range(1, 4):
                direction = number_to_direction(move)
                x_new = x + direction[0]
                y_new = y + direction[1]
                if 0 <= x_new < x_grid_size and 0 <= y_new < y_grid_size and grid[x_new][y_new] != 0:
                    neighbors.append(move)

            if (len(neighbors)) == 0:
                continue

            move = random.choice(neighbors)
            direction = number_to_direction(move)
            grid[x][y] = move
            # raczej zbędna linia
            # grid[x+direction[0]][y+direction[1]] = opposite_move(move)
            return [x, y]


def generate_maze(x_size: int, y_size: int) -> []:
    grid = [[0] * y_size for _ in range(x_size)]
    point = [random.randint(1, x_size - 1), random.randint(1, y_size - 1)]

    while point is not None:
        point = walk(grid, point[0], point[1], x_size, y_size)
        if point is None:
            point = hunt(grid, x_size, y_size)
    return grid


def print_maze(grid: [], x_size: int, y_size: int):
    transposed_grid = [[grid[j][i] for j in range(x_size)] for i in range(y_size)]
    x_size_copy = x_size
    x_size = y_size
    y_size = x_size_copy

    # powiększam grid o 1 w każdą stronę, żeby poprawnie móc wyprintować labirynt
    maze_to_print = [[3] * (y_size + 1) for _ in range(x_size + 1)]
    maze_to_print[0][0] = 0
    # 1 - dolna ściana, 2 - prawa ściana, 3 - obie ściany
    for x in range(x_size):
        maze_to_print[x + 1][0] = 2
    for y in range(y_size):
        maze_to_print[0][y + 1] = 1

    for x in range(x_size):
        for y in range(y_size):
            x_new = x + 1
            y_new = y + 1
            move = transposed_grid[x][y]
            if move == 2:
                maze_to_print[x_new][y_new] -= 2
            elif move == 3:
                maze_to_print[x_new][y_new] -= 1
            elif move == 1:
                maze_to_print[x_new - 1][y_new] -= 2
            elif move == 4:
                maze_to_print[x_new][y_new - 1] -= 1

    for x in range(x_size + 1):
        line = ''
        for y in range(y_size + 1):
            walls = maze_to_print[x][y]
            if walls == 1:
                line += '__'
            elif walls == 2:
                line += '|'
            elif walls == 3:
                line += '_|'
            else:
                line += '  '
        print(line)


def main():
    x_size = 3
    y_size = 6
    maze = generate_maze(x_size, y_size)
    print_maze(maze, x_size, y_size)


if __name__ == '__main__':
    main()
