#!/usr/bin/python3
# Author: Konrad Micek, Applied Computer Science, Bachelors degree 1st year

import tkinter
from PIL import ImageTk, Image
from tkinter import messagebox
import sys

from python_maze_printer import MazePrinter


def integer_check(in_str, acttyp):
    if acttyp == '1':  # insert
        if not in_str.isdigit():
            return False
    return True


def rescale_image(image: Image):
    max_x = window.bbox(0, 0)[2]
    max_y = window.winfo_height()
    x_ratio = max_x / image.width
    y_ratio = max_y / image.height
    ratio = x_ratio if x_ratio < y_ratio else y_ratio
    return ImageTk.PhotoImage(image.resize((int(image.width * ratio), int(image.height * ratio)), Image.LANCZOS))


def btn_resolve_callback():
    img = rescale_image(printer.resolve_maze())
    label_image.configure(image=img)
    label_image.image = img
    # refreshes size of label containing image
    window.update_idletasks()


def btn_generate_callback():
    x = int(entry_xsize.get())
    y = int(entry_ysize.get())
    if x < 4 or x > 100 or y < 4 or y > 100:
        tkinter.messagebox.showerror('Error', 'Wrong size of maze. X and Y should be from interval <4, 100>.')
        return

    # overwrite old printer instance
    global printer
    printer = MazePrinter(x, y)
    img = rescale_image(printer.generate_image([]))
    label_image.configure(image=img)
    label_image.image = img
    # refreshes size of label containing image
    button_resolve.config(state='normal')
    window.update_idletasks()


if '-h' in sys.argv or '--help' in sys.argv:
    print("Application goal is to generate mazes with size specified by user and allow him to resolve it programmatically.")
    print("Different application parts are built in Python (GUI/languages connector), Perl (generator) and Bash (resolver).")
    print("Bash solving takes some time - it is Bash, so it obviously have right to be slow :-)")
    print("After generation, picture is saved as file MazeUnresolved.jpeg.")
    print("After resolving, picture is saved as file MazeResolved.jpeg.")
    print("Picture is also shown in GUI.")
    print("Requirements:")
    print("For proper working, user should have installed packages PIL (Pillow) and Tkinter.")
    print("User should run application on Linux capable of running GUI.")
    print("For guaranted experience use the newest version of Python.")
    exit()

if sys.stdin.isatty():
    print('Application started from TTY without GUI, so it cannot start its GUI. Exiting application...')
    exit(1)

try:
    printer: MazePrinter

    window = tkinter.Tk()
    window.title("Maze generator & resolver")
    # zoomed and not resizable
    window.attributes('-zoomed', True)
    window.state('iconic')
    window.resizable(False, False)
    window.columnconfigure(0, weight=11)
    window.columnconfigure(1, weight=1)

    label_xsize = tkinter.Label(window, text="X size:")
    label_xsize.grid(column=1, row=0)
    label_xsize.config(font=("Calibri", 22))
    entry_xsize = tkinter.Entry(window, validate="key", width=10)
    entry_xsize.grid(column=1, row=1, padx=10, pady=5)
    entry_xsize.config(font=("Calibri", 22))
    entry_xsize['validatecommand'] = (entry_xsize.register(integer_check), '%P', '%d')
    entry_xsize.insert(0, '11')

    label_ysize = tkinter.Label(window, text="Y size:")
    label_ysize.grid(column=1, row=2)
    label_ysize.config(font=("Calibri", 22))
    entry_ysize = tkinter.Entry(window, validate="key", width=10)
    entry_ysize.grid(column=1, row=3, padx=10, pady=5)
    entry_ysize.config(font=("Calibri", 22))
    entry_ysize['validatecommand'] = (entry_ysize.register(integer_check), '%P', '%d')
    entry_ysize.insert(0, '12')

    button_generate = tkinter.Button(window, text="Generate maze", command=btn_generate_callback)
    button_generate.grid(column=1, row=4, padx=10, pady=10)
    button_generate.config(font=("Calibri", 22), height=2)

    button_resolve = tkinter.Button(window, text="Resolve maze", command=btn_resolve_callback)
    button_resolve.grid(column=1, row=5, padx=10, pady=10)
    button_resolve.config(font=("Calibri", 22), height=2, state='disabled')
except:
    print('Problem with Tkinter - it is probably not installed. Exiting application...')
    exit(1)

try:
    # initially transparent image
    img = ImageTk.PhotoImage(Image.new('RGBA', (200, 50)))
    label_image = tkinter.Label(window, image=img)
    label_image.grid(column=0, row=0, rowspan=66)
except:
    print('Problem with PIL (Pillow) - it is probably not installed. Exiting application...')
    exit(1)


window.mainloop()
