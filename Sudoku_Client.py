from __future__ import print_function

import sys, os
import pygame               # Must install pygame for this module to work (see Manual)
sys.path.append(os.path.join("objects"))
sys.path.append(os.path.join("Server Side"))
sys.path.append(os.path.join("Client Side"))


from socket import socket, AF_INET, SOCK_DGRAM
from GameResources import *
import Reception_Handler
import select, socket, sys
import pychat_util
import threading
import time
from xmlrpclib import ServerProxy
import serverdisc
import roomsgui


import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOG = logging.getLogger()



from Tkinter import *
import tkMessageBox as messagebox
import Tkinter as tk
import sys


###############################################################################

'''
Sudoku Client script handles the initial server connection 
and resolves the protocols. When the client is assigned a room
and a game this script runs two threads:

1- For continous reception of Grid Updation from server
2- Game Logic and GUI of Client Handler
'''

###############################################################################


UserName=''
Inputs_Done=False
proxy=None      # SimpleXMLRPC Proxy variable


# Discovered Server-Ip
MAGIC = "fna349fn" #to make sure we don't confuse or get confused by other programs
server_ip=None
server_port=None


###############################################################################


def Try_Discovering_Server():
    global MAGIC
    global server_ip
    global server_port

    s = socket.socket(AF_INET, SOCK_DGRAM)  # create UDP socket
    s.bind(('', 12346))

    while 1:
        data, addr = s.recvfrom(1024)  # wait for a packet
        if data.startswith(MAGIC):

            LOG.info("Got service announcement from %s"%data[len(MAGIC):])
            addr_port = str(data[len(MAGIC):]).split(' ');
            server_ip=addr_port[0]
            server_port=(int)(str(addr_port[1]))
            s.close()
            break


def create_window():

    window = tk.Toplevel()



"""
A recursive method running under reception thread
to recive continous updated grid from server.
"""

def refresh_query():
    time.sleep(1)
    try:
        grid = proxy.Get_Grid(roomsgui.selected_room)
        for i in range(9):
            for j in range(9):
                if(Reception_Handler.MainGrid[i][j] is not grid[i][j]):
                    x= 9*(i)
                    y= x+j
                    Reception_Handler.theSquares[y].change(grid[i][j])
        Reception_Handler.MainGrid = grid
    except:
        pass


    refresh_query()


#=================================================================================================



'''
The openServer calls server discovery window from serverdisc module
'''
def openServer(won,username=None):
    global UserName
    UserName=username
    serverdisc.ServerDiscoveryWindow(server_ip,server_port,UserName,won)


'''
The save function saves a new player name. It also checks if a name already exists and avoids adding duplicate player name.
'''

def save(player):
    text = player.get()
    data = open('Player_Name.txt',"r+")
    f = list(data.read().split())
    #print (f)
    for nicknames in f:
        if text in f:
            print ("Nickname already exists")
            messagebox.showinfo('Error','Nickname already exists')
            break
        else:
            data.write(text+"\n")
            print ("New name added")
            break
    #print (nicknames)
    return text

#=================================================================================================


def Check_Inputs():
    global proxy
    global UserName

    while(roomsgui.selected_room==None):

        time.sleep(1)
    # print("GOt it..")
    proxy = roomsgui.proxy
    grid=None
    if(roomsgui.join):
        grid=proxy.join_room(UserName,roomsgui.selected_room)
    else:
        grid=proxy.create_room(UserName,roomsgui.selected_room)

    handle = Reception_Handler.Handler()  # Client Handler Handle class object

    # Threads to operate client's reception and game GUI
    game = threading.Thread(target=handle.Initial_Reception, args=(grid,UserName,proxy))
    refreshloop = threading.Thread(target=refresh_query)
    game.start()
    refreshloop.start()
    game.join()
    refreshloop.join()

    Reception_Handler.inroom=True


#=================================================

'''
The makeWindow() function creates the GUI interface using Tkinter widgets. All widgets are activated or displayed by calling the pack function,
which is a default function for every widget is called.
'''

def makeWindow():
    global nameVar, namSugg

    def onselect(evt):
        # Note here that Tkinter passes an event object to onselect()
        global UserName

        name.delete(0,END)
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        # print('You selected item %d: "%s"' % (index, value))
        UserName=value;
        # print(UserName)
        name.insert(0,value)


    won = Tk()
    won.title('Sudoku')
    Label(won, text = 'Welcome to Sudoku world').pack(pady = 30)
    won.geometry('500x400')

    frame1 = Frame(won)
    frame1.pack()
    C = Canvas()
    Label(frame1, text = 'Player Name').grid(row = 0, column = 0, sticky = W)
    nameVar = StringVar()
    namSugg = StringVar()

    name = Entry(frame1, textvariable = nameVar)
    name.grid(row = 0, column = 1, sticky = W)


    frame2 = Frame(won, width = 200, height = 100)
    scrollbar = Scrollbar(won)
    scrollbar.pack(side = RIGHT, fill = Y)

    listbox = Listbox(frame2, yscrollcommand = scrollbar.set)
    listbox.bind('<<ListboxSelect>>', onselect)
    f = open('Player_Name.txt').readlines()
    for word in f:
        item = word
        item = item[0:len(item)-1]
        listbox.insert(END, item)
        listbox.pack(side = LEFT, fill = BOTH)
        scrollbar.config(command = listbox.yview)

    C.pack(pady = 40)
    b = Button(C, text = 'Save Player', command = lambda:save(nameVar))
    b1 = Button(C, text = 'Enter', command = lambda:openServer(won,name.get()))
    b4 = Button(C, text = 'Cancel', command = lambda:exit(sys))
    b.pack(side = LEFT, padx = 20)
    b1.pack(side = LEFT, padx = 20)
    b4.pack(side = RIGHT, padx = 20)
    frame2.pack()
    return won





# Threads for server discovery over the network
discover = threading.Thread(target=Try_Discovering_Server)
discover.start()


# Threads to check if GUI inputs are done
Check = threading.Thread(target=Check_Inputs)
Check.start()

won = makeWindow()
won.mainloop()


