#!/usr/bin/python3
# Author: Konrad Micek, Applied Computer Science, Bachelors degree 1st year

import random
import subprocess
import sys

from PIL import Image, ImageDraw

if '-h' in sys.argv or '--help' in sys.argv:
    print("Application goal is to generate mazes with size specified by user and allow him to resolve it programmatically.")
    print("Different application parts are built in Python (GUI/languages connector), Perl (generator) and Bash (resolver).")
    print("Bash solving takes some time - it is Bash, so it obviously have right to be slow :-)")
    print("After generation, picture is saved as file MazeUnresolved.jpeg.")
    print("After resolving, picture is saved as file MazeResolved.jpeg.")
    print("Picture is also shown in GUI.")
    exit()
elif not any('python_gui.py' in s for s in sys.argv):
    print("That script won't run separately from Python GUI. Starting Python GUI script instead...")
    subprocess.Popen(['./python_gui.py'])
    exit()

class MazePrinter:
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.block_size = 16
        self.grid = self.generate_maze()
        self.walls = self.convert_to_walls(self.grid)
        self.apertures = self.add_apertures()

    def generate_image(self, path):
        # +3, bcs white line adds space
        img = Image.new(mode='RGB', size=(self.block_size * (self.x_size - 1) + 3, self.block_size * (self.y_size - 1) + 3))
        draw = ImageDraw.Draw(img)

        for y in range(self.y_size):
            for x in range(self.x_size):
                if x > 0 and y > 0 and len(path) > 0:
                    index1d = str((y - 1) * (self.x_size - 1) + x - 1)
                    if index1d in path:
                        self.insert_path(draw, x, y)
                if self.walls[x][y] == 1 or self.walls[x][y] == 3:
                    self.insert_wall(draw, x, y, False)
                if self.walls[x][y] == 2 or self.walls[x][y] == 3:
                    self.insert_wall(draw, x, y, True)

        if len(path) > 0:
            img.save('MazeUnresolved.jpeg', 'JPEG')
        else:
            img.save('MazeResolved.jpeg', 'JPEG')
        return img

    def insert_wall(self, draw: ImageDraw, x: int, y: int, vertical: bool):
        start_x = self.block_size * x
        start_y = self.block_size * y
        if vertical:
            draw.rectangle(((start_x, (start_y - self.block_size)), (start_x + 2, (start_y + 18 - self.block_size))), fill="red")
        else:
            draw.rectangle((((start_x - self.block_size), start_y), ((start_x - self.block_size) + 18, start_y + 2)), fill="red")

    def insert_path(self, draw: ImageDraw, x: int, y: int):
        start_x = self.block_size * (x - 1)
        start_y = self.block_size * (y - 1)
        draw.rectangle(((start_x + 3, start_y + 3), (start_x + self.block_size + 2, start_y + self.block_size + 2)), fill="green")

    def convert_to_walls(self, grid):
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
                    move = grid[x][y] & 1 << i
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

    def add_apertures(self):
        aperture1 = random.randint(1, self.x_size - 1)
        self.walls[aperture1][0] -= 1
        aperture2 = random.randint(1, self.x_size - 1)
        self.walls[aperture2][self.y_size - 1] -= 1
        return [[aperture1, 0], [aperture2, self.y_size - 1]]

    def get_2d_grid(self, stdout: str, x_size: int, y_size: int):
        splitted_stdout = stdout.strip().split(' ')
        result = [[0] * y_size for _ in range(x_size)]
        for i in range(len(splitted_stdout)):
            y = int(i / x_size)
            x = i % x_size
            result[x][y] = int(splitted_stdout[i])
        return result

    def generate_maze(self):
        # run Perl script and get its STDOUT
        result = subprocess.run(['./perl_maze_generator.pl', str(self.x_size), str(self.y_size)], stdout=subprocess.PIPE, text=True)
        grid = self.get_2d_grid(result.stdout, self.x_size, self.y_size)
        return grid

    def resolve_maze(self):
        # run Bash script and get its STDOUT
        # -1, bcs I appended maze by 1 in x and y for proper printing
        args = ['./bash_maze_solver.sh', str(self.x_size - 1), str(self.y_size - 1), str(self.apertures[0][0] - 1), str(self.apertures[0][1]),
                str(self.apertures[1][0] - 1), str(self.apertures[1][1] - 1)]
        for y in range(self.y_size - 1):
            for x in range(self.x_size - 1):
                args.append(str(self.grid[x][y]))
        res = subprocess.run(args, stdout=subprocess.PIPE, text=True)
        path = res.stdout.split('Results:')[-1]
        return self.generate_image(path.split(' '))
