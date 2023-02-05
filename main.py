import tkinter
from PIL import ImageTk, Image
from tkinter import messagebox

from maze_printer import MazePrinter


def integer_check(in_str, acttyp):
    if acttyp == '1':  # insert
        if not in_str.isdigit():
            return False
    return True


def btn_resolve_callback():
    #printer.resolve_maze()
    print()


def btn_generate_callback():
    x = int(entry_xsize.get())
    y = int(entry_ysize.get())
    if x < 4 or x > 1000 or y < 4 or y > 1000:
        tkinter.messagebox.showerror('Error', 'Wrong size of maze. X and Y should be from interval <4, 1000>.')
        return

    printer = MazePrinter(x, y)
    img = ImageTk.PhotoImage(printer.generate_image())
    #wpercent = (basewidth / float(img.size[0]))
    #hsize = int((float(img.size[1]) * float(wpercent)))
    #img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)

    label_image.configure(image=img)
    label_image.image = img
    # refreshes size of label containing image
    window.update_idletasks()
    print(label_image.winfo_height())
    print(label_image.winfo_width())
    print(window.winfo_width())
    print(window.winfo_height())

window = tkinter.Tk()
window.title("Maze generator & resolver")
# zoomed and not resizable
window.attributes('-zoomed', True)
window.resizable(False, False)
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

button_generate = tkinter.Button(window, text="Generate maze", command=btn_generate_callback)
button_generate.grid(column=1, row=4, padx=10, pady=10, sticky=tkinter.EW)
button_generate.config(font=("Calibri", 22), height=2)

button_resolve = tkinter.Button(window, text="Resolve maze", command=btn_resolve_callback)
button_resolve.grid(column=1, row=5, padx=10, pady=10, sticky=tkinter.EW)
button_resolve.config(font=("Calibri", 22), height=2)

# initially transparent image
img = ImageTk.PhotoImage(Image.new('RGBA', (200, 50)))
label_image = tkinter.Label(window, image=img)
label_image.grid(column=0, row=0, rowspan=66)

window.mainloop()
