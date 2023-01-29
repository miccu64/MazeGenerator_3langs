import tkinter
from tkinter import messagebox
import subprocess
import maze_worker
from PIL import ImageTk, Image

from maze_printer import MazePrinter


def integer_check(in_str, acttyp):
    if acttyp == '1':  # insert
        if not in_str.isdigit():
            return False
    return True


def get_2d_grid(stdout: str, x_size: int, y_size: int):
    splitted_stdout = stdout.split(' ')
    result = [[0] * y_size for _ in range(x_size)]
    for i in range(len(splitted_stdout) - 1):
        y = int(i / x_size)
        x = i % x_size
        result[x][y] = int(splitted_stdout[i])
    return result


def button_callback():
    x = int(entry_xsize.get())
    y = int(entry_ysize.get())
    if x < 4 or x > 1000 or y < 4 or y > 1000:
        tkinter.messagebox.showerror('Error', 'Wrong size of maze. X and Y should be from interval <4, 1000>.')
        return
    # run Perl script and get its STDOUT
    result = subprocess.run(['./perl_maze_generator.pl', str(x), str(y)], stdout=subprocess.PIPE, text=True)
    grid = get_2d_grid(result.stdout, x, y)
    maze_worker.print_maze(grid, x, y)

    printer = MazePrinter(grid)
    printer.generate_image()


window = tkinter.Tk()
window.title("Maze generator & resolver")
# window.attributes('-zoomed', True)
window.columnconfigure(0, weight=11)
window.columnconfigure(1, weight=1)

label_xsize = tkinter.Label(window, text="X size:")
label_xsize.grid(column=1, row=0, sticky=tkinter.EW)
label_xsize.config(font=("Calibri", 22))
entry_xsize = tkinter.Entry(window, validate="key")
entry_xsize.grid(column=1, row=1, sticky=tkinter.E, padx=10, pady=5)
entry_xsize.config(font=("Calibri", 22))
entry_xsize['validatecommand'] = (entry_xsize.register(integer_check), '%P', '%d')
entry_xsize.insert(0, '4')

label_ysize = tkinter.Label(window, text="Y size:")
label_ysize.grid(column=1, row=2, sticky=tkinter.EW)
label_ysize.config(font=("Calibri", 22))
entry_ysize = tkinter.Entry(window, validate="key")
entry_ysize.grid(column=1, row=3, sticky=tkinter.E, padx=10, pady=5)
entry_ysize.config(font=("Calibri", 22))
entry_ysize['validatecommand'] = (entry_ysize.register(integer_check), '%P', '%d')
entry_ysize.insert(0, '5')

button_generate = tkinter.Button(window, text="Generate maze", command=button_callback)
button_generate.grid(column=1, row=4, padx=10, pady=10, sticky=tkinter.EW)
button_generate.config(font=("Calibri", 22), height=2)

# initially transparent image
img = ImageTk.PhotoImage(Image.new('RGBA', (200, 50)))
label_image = tkinter.Label(window, image=img)
label_image.grid(column=0)
print(label_image.size)
window.mainloop()
