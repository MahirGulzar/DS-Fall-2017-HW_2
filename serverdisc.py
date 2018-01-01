from tkinter import *
import tkinter.messagebox
from tkinter import font  as tkfont
import roomsgui


def func2():
    roomsgui.main()
# master = Tk()
# Label(master, text="server discovery").grid(row=0)
# Button(master, text='Enter').grid(row=3, column=1, sticky=W, pady=4)
def func():
    master = Tk()
    Label(master, text="server discovery").grid(row=0)
    Button(master, text='Enter', command=func2).grid(row=3, column=1, sticky=W, pady=4)
    mainloop()

