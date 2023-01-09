import random

# http://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm
def number_to_direction(numb: int) -> [int]:
    if numb == 1:
        return [-1, 0]
    if numb == 2:
        return [1, 0]
    if numb == 3:
        return [0, 1]
    if numb == 4:
        return [0, -1]


def random_move(used_moves: [int]) -> int:
    if (len(used_moves)) == 4:
        return 0
    while True:
        new_direction = random.randint(1, 4)
        if new_direction not in used_moves:
            return new_direction


def walk(grid: [], current_x: int, current_y: int, x_grid_size: int, y_grid_size: int) -> None:
    used_moves = []
    while len(used_moves) < 4:
        move = random_move(used_moves)
        used_moves.append(move)
        direction = number_to_direction(move)
        new_x = current_x + direction[0]
        new_y = current_y + direction[1]
        if new_x < 0 or new_y < 0 or new_x >= x_grid_size or new_y >= y_grid_size or grid[new_x][new_y] != 0:
            continue


xsize = 10
ysize = 10
