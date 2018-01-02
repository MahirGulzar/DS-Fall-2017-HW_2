from tkinter import *
import tkinter.messagebox
from tkinter import font  as tkfont
import roomsgui


def func2(server_ip,server_port,username,win):
    win.destroy()
    roomsgui.main(server_ip,server_port,username)

def func(server_ip,server_port,username,won):
    won.destroy()
    master = Tk()
    master.geometry("500x400")
    master.title("Server Discovery")
    # Label(master, text="server discovery").grid(row=3, column=1)
    item="Found Server at IP: "+str(server_ip)+"  PORT:"+str(server_port)
    Label(master, text=item).grid(row=0, column=2)
    Button(master, text='Enter', command=lambda:func2(server_ip,server_port,username,master)).grid(row=1, column=2, sticky=W, pady=4)


