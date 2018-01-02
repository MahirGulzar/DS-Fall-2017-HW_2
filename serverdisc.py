from tkinter import *
import tkinter.messagebox
from tkinter import font  as tkfont
import roomsgui


'''
    Create Roomlist GUI after user presses enter on server discovery
'''
def RoomGUIWindow(server_ip,server_port,username,win):
    win.destroy()       # Destroy previous window
    roomsgui.main(server_ip,server_port,username)

'''
    ServerDiscovery Window tells user the discovered server Ip and port
'''
def ServerDiscoveryWindow(server_ip,server_port,username,won):
    won.destroy()       # Destroy previous window
    master = Tk()
    master.geometry("500x400")
    master.title("Server Discovery")
    item="Found Server at IP: "+str(server_ip)+"  PORT:"+str(server_port)
    Label(master, text=item).grid(row=0, column=2)
    Button(master, text='Enter', command=lambda:RoomGUIWindow(server_ip,server_port,username,master)).grid(row=1, column=2, sticky=W, pady=4)


