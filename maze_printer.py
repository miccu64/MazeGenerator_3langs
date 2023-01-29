from PIL import Image, ImageDraw


class MazePrinter:
    def __init__(self, grid):
        self.grid = grid
        self.x_size = len(grid)
        self.y_size = len(grid[0])
        self.block_size = 16
        self.walls = self.convert_to_walls()

    def generate_image(self):
        # +3, bcs white line adds space
        img = Image.new(mode='RGB', size=(self.block_size * (self.x_size - 1) + 3, self.block_size * (self.y_size - 1) + 3))
        draw = ImageDraw.Draw(img)

        for y in range(self.y_size):
            for x in range(self.x_size):
                if self.walls[x][y] == 1 or self.walls[x][y] == 3:
                    self.insert_wall(draw, x, y, False)
                if self.walls[x][y] == 2 or self.walls[x][y] == 3:
                    self.insert_wall(draw, x, y, True)

        img.save('MazeUnresolved.jpeg', 'JPEG')
        img.show()

    def insert_wall(self, draw: ImageDraw, x: int, y: int, vertical: bool):
        start_x = self.block_size * x
        start_y = self.block_size * y

        if vertical:
            draw.rectangle(((start_x, (start_y - self.block_size)), (start_x + 2, (start_y + 18 - self.block_size))), fill="white")
        else:
            draw.rectangle((((start_x - self.block_size), start_y), ((start_x - self.block_size) + 18, start_y + 2)), fill="white")

    def convert_to_walls(self):
        # append grid by 1 in x and y to properly print maze
        maze_to_print = [[3] * (self.y_size + 1) for _ in range(self.x_size + 1)]
        # 1 - bottom wall, 2 - right wall, 3 - both walls
        for x in range(self.x_size + 1):
            maze_to_print[x][0] = 1
        for y in range(self.y_size + 1):
            maze_to_print[0][y] = 2
        maze_to_print[0][0] = 0

        for x in range(self.x_size):
            for y in range(self.y_size):
                x_new = x + 1
                y_new = y + 1
                for i in range(0, 3):
                    # bit shifting
                    move = self.grid[x][y] & 1 << i
                    if move == 2 and (maze_to_print[x_new][y_new] == 2 or maze_to_print[x_new][y_new] == 3):
                        maze_to_print[x_new][y_new] -= 2
                    elif move == 4 and (maze_to_print[x_new][y_new] == 1 or maze_to_print[x_new][y_new] == 3):
                        maze_to_print[x_new][y_new] -= 1
                    elif move == 1 and (maze_to_print[x_new - 1][y_new] == 2 or maze_to_print[x_new - 1][y_new] == 3):
                        maze_to_print[x_new - 1][y_new] -= 2
                    elif move == 8 and (maze_to_print[x_new][y_new - 1] == 1 or maze_to_print[x_new][y_new - 1] == 3):
                        maze_to_print[x_new][y_new - 1] -= 1
        # adding 1, bcs walls needs 1 bigger size in each dimension
        self.x_size += 1
        self.y_size += 1
        return maze_to_print
