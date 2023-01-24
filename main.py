import random


# Hunt and Kill algorithm
# http://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm


# 1 -> left, 2 -> right, 4 -> down, 8 -> up
def number_to_direction(numb: int):
    if numb == 1:
        return [-1, 0]
    if numb == 2:
        return [1, 0]
    if numb == 4:
        return [0, 1]
    if numb == 8:
        return [0, -1]


def opposite_move(numb: int):
    if numb == 1:
        return 2
    if numb == 2:
        return 1
    if numb == 4:
        return 8
    if numb == 8:
        return 4


def random_move(used_moves) -> int:
    if (len(used_moves)) == 4:
        return 0

    new_direction = 0
    while new_direction == 0 or new_direction in used_moves:
        new_direction = random.randint(0, 3)
        new_direction = 2 ** new_direction
    return new_direction


def walk(grid, current_x: int, current_y: int, x_grid_size: int, y_grid_size: int):
    used_moves = []
    while len(used_moves) < 4:
        move = random_move(used_moves)
        used_moves.append(move)
        direction = number_to_direction(move)
        new_x = current_x + direction[0]
        new_y = current_y + direction[1]
        if new_x < 0 or new_y < 0 or new_x >= x_grid_size or new_y >= y_grid_size or grid[new_x][new_y] != 0:
            continue
        grid[current_x][current_y] += move
        grid[new_x][new_y] += opposite_move(move)
        return [new_x, new_y]


def hunt(grid, x_grid_size: int, y_grid_size: int):
    for x in range(x_grid_size):
        for y in range(y_grid_size):
            if grid[x][y] != 0:
                continue
            neighbors = []

            for move_pow in range(0, 3):
                move = 2 ** move_pow
                direction = number_to_direction(move)
                x_new = x + direction[0]
                y_new = y + direction[1]
                if 0 <= x_new < x_grid_size and 0 <= y_new < y_grid_size and grid[x_new][y_new] != 0:
                    neighbors.append(move)

            if (len(neighbors)) == 0:
                continue

            move = random.choice(neighbors)
            direction = number_to_direction(move)
            grid[x][y] += move
            grid[x+direction[0]][y+direction[1]] += opposite_move(move)
            # transposed_grid = [[grid[j][i] for j in range(x_grid_size)] for i in range(y_grid_size)]

            return [x, y]


def generate_maze(x_size: int, y_size: int):
    grid = [[0] * y_size for _ in range(x_size)]
    point = [random.randint(0, x_size - 1), random.randint(0, y_size - 1)]

    while point is not None:
        point = walk(grid, point[0], point[1], x_size, y_size)
        if point is None:
            point = hunt(grid, x_size, y_size)
    return grid


def print_maze(grid, x_size: int, y_size: int):
    # append grid by 1 in x and y to properly print maze
    maze_to_print = [[3] * (y_size + 1) for _ in range(x_size + 1)]
    # 1 - bottom wall, 2 - right wall, 3 - both walls
    for x in range(x_size + 1):
        maze_to_print[x][0] = 1
    for y in range(y_size + 1):
        maze_to_print[0][y] = 2
    maze_to_print[0][0] = 0

    for x in range(x_size):
        for y in range(y_size):
            x_new = x + 1
            y_new = y + 1
            for i in range(0, 3):
                move = grid[x][y] & 1 << i
                if move == 2 and (maze_to_print[x_new][y_new] == 2 or maze_to_print[x_new][y_new] == 3):
                    maze_to_print[x_new][y_new] -= 2
                elif move == 4 and (maze_to_print[x_new][y_new] == 1 or maze_to_print[x_new][y_new] == 3):
                    maze_to_print[x_new][y_new] -= 1
                elif move == 1 and (maze_to_print[x_new - 1][y_new] == 2 or maze_to_print[x_new - 1][y_new] == 3):
                    maze_to_print[x_new - 1][y_new] -= 2
                elif move == 8 and (maze_to_print[x_new][y_new - 1] == 1 or maze_to_print[x_new][y_new - 1] == 3):
                    maze_to_print[x_new][y_new - 1] -= 1

    for y in range(y_size + 1):
        line = ''
        for x in range(x_size + 1):
            walls = maze_to_print[x][y]
            if walls == 1:
                line += '__'
            elif walls == 2:
                line += ' |'
            elif walls == 3:
                line += '_|'
            else:
                line += '  '
        print(line)


def solve_maze(x_size: int, y_size: int, x_start: int, y_start: int, x_end: int, y_end: int, grid):
    flattened_grid = []
    for y in range(y_size):
        for x in range(x_size):
            flattened_grid.append(grid[x][y])

    a=0


def main():
    x_size = 4
    y_size = 5
    maze = generate_maze(x_size, y_size)
    print_maze(maze, x_size, y_size)


if __name__ == '__main__':
    main()
