import tkinter
from tkinter import messagebox


def integer_check(in_str, acttyp):
    if acttyp == '1':  # insert
        if not in_str.isdigit():
            return False
    return True


def button_callback():
    x = int(entry_xsize.get())
    y = int(entry_ysize.get())
    if x < 4 or x > 1000 or y < 4 or y > 1000:
        tkinter.messagebox.showerror('Error', 'Wrong size of maze. X and Y should be from interval <4, 1000>.')


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
entry_xsize.insert(0, '10')

label_ysize = tkinter.Label(window, text="Y size:")
label_ysize.grid(column=1, row=2, sticky=tkinter.EW)
label_ysize.config(font=("Calibri", 22))
entry_ysize = tkinter.Entry(window, validate="key")
entry_ysize.grid(column=1, row=3, sticky=tkinter.E, padx=10, pady=5)
entry_ysize.config(font=("Calibri", 22))
entry_ysize['validatecommand'] = (entry_ysize.register(integer_check), '%P', '%d')
entry_ysize.insert(0, '10')

button_generate = tkinter.Button(window, text="Generate maze", command=button_callback)
button_generate.grid(column=1, row = 4, pady=10)
button_generate.config(font=("Calibri", 22), height=2)


window.mainloop()
