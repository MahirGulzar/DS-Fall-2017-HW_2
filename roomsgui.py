from tkinter import *
import tkinter.messagebox
from tkinter import font  as tkfont

def show_entry_fields():
   x=(e1.get())
   flag=1
   f = open("rooms.txt", "a+")
   f2 = open("rooms.txt","r")
   contents=f2.read().split("\n")
   for con in xrange(len(contents)):
       if x==contents[con]:
           flag=0
           break
   if flag == 0:
         tkinter.messagebox.showinfo("error", "Room name already exists")
   else:
       f.write(x)
       f.write("\n")
       print "yes"
       e1.delete(0,END)

def main():
    f3 = open("roomnames.txt", "r")
    suggested_names = f3.read().split("\n")
    master = Tk()
    Label(master, text="room Name").grid(row=0)
    # Results = Label(master, text = "suggested names:%s" %suggested_names)
    # Results.grid(row = 1, column = 1)
    f3 = open("roomnames.txt", "r")
    suggested_names = f3.read().split("\n")

    e1 = Entry(master)
    e1.insert(10, "")

    e1.grid(row=0, column=1)

    Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
    Button(master, text='Enter', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)

    mainloop()

