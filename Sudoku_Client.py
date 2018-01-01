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


import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOG = logging.getLogger()



from Tkinter import *
import tkMessageBox as messagebox
import Tkinter as tk
import sys
#import Sudoku_Client


###############################################################################

'''
Sudoku Client script handles the initial server connection 
and resolves the protocols. When the client is assigned a room
and a game this script runs two threads:

1- For continous reception of Grid Updation from server
2- Game Logic and GUI of Client Handler
'''


'''
This is the user interface code for Sudoku GUI. It asks for a player name first and saves the player name
in a txt file. If a player has already saved his/her name, the player can select his/her name from a listbox appearing
in the main window.
'''

UserName=''
Sname=''
Pname=''
Inputs_Done=False
proxy=None


# Discovered Server-Ip
MAGIC = "fna349fn" #to make sure we don't confuse or get confused by other programs
server_ip=None
server_port=None


def Try_Discovering_Server():
    global MAGIC
    global server_ip
    global server_port

    s = socket.socket(AF_INET, SOCK_DGRAM)  # create UDP socket
    s.bind(('', 19191))

    while 1:
        data, addr = s.recvfrom(1024)  # wait for a packet
        if data.startswith(MAGIC):

            LOG.info("Got service announcement from %s"%data[len(MAGIC):])
            addr_port = str(data[len(MAGIC):]).split(' ');
            server_ip=addr_port[0]
            server_port=(int)(str(addr_port[1]))
            break


def create_window():

    window = tk.Toplevel()



"""
A recursive method running under reception thread
to recive continous updated grid from server.
"""

def refresh_query():
    time.sleep(1)
    msg='refresh:'
    try:
        grid = proxy.Get_Grid("custom_room")
        # print("Grid:\n")
        # print(grid[0][0])
        # print(grid[0][1])
        # print(grid[0][2])
        #
        # print("Main:\n")
        # print(Reception_Handler.MainGrid[0][0])
        # print(Reception_Handler.MainGrid[0][1])
        # print(Reception_Handler.MainGrid[0][2])

        for i in range(9):
            for j in range(9):
                if(Reception_Handler.MainGrid[i][j] is not grid[i][j]):
                    # print("Old = ", Reception_Handler.MainGrid[i][j])
                    # print("New = ",grid[i][j])
                    x= 9*(i)
                    y= x+j
                    Reception_Handler.theSquares[y].change(grid[i][j])
                    # print('i  and j = ',i,j)
                    # print('location = %d'%y)
                    # print('number = ',grid[i][j])
        Reception_Handler.MainGrid = grid
    except:
        pass


    refresh_query()


'''
The openServer functions executes, when the player name is accepted. It opens a new python window where the player need to specify
the server address and port number.
'''
def openServer(player):

    global UserName
    UserName = player.get()
    UserName = player.get()
    #print(UserName)

    '''
    The create_window() function creates a window.
    '''

    def create_window():
        window = tk.Toplevel()

    def save1(sname, pname):
        global Inputs_Done
        global won
        global server_port
        global server_ip
        Inputs_Done=True
        win.destroy()
        won.destroy()
        serverdisc.func()
        # TODO
        # Server Discovery window
        # Room Selections window (Create and Join)
        # Start Game

        if(server_port==None):
            LOG.info('Server not Found yet trying running server first.. Quiting Application now..')
            sys.exit(2)
        global proxy
        # RPC Server's socket address
        server = (server_ip, server_port)

        try:
            proxy = ServerProxy("http://%s:%d" % server)
        except KeyboardInterrupt:
            LOG.warn('Ctrl+C issued, terminating')
            exit(0)
        except Exception as e:
            LOG.error('Communication error %s ' % str(e))
            exit(1)

        LOG.info('Connected to File XMLRPC server!')
        methods = filter(lambda x: 'system.' not in x, proxy.system.listMethods())
        LOG.debug('Remote methods are: [%s] ' % (', '.join(methods)))

        check, data = proxy.Welcome_and_getList("Mahir", 23212)
        grid = proxy.join_room("ali", "custom_room")
        handle = Reception_Handler.Handler()  # Client Handler Handle class object

        # Threads to operate client's reception and game GUI
        game = threading.Thread(target=handle.Initial_Reception, args=(grid,UserName,proxy))
        refreshloop = threading.Thread(target=refresh_query)
        game.start()
        refreshloop.start()
        game.join()
        refreshloop.join()

        Reception_Handler.inroom=True


    '''
    The makeWindow() function creates the GUI interface using Tkinter widgets. All widgets are activated or displayed by calling the pack function,
    which is a default function for every widget is called.
    '''

    def makeWindow():
        global Sname, Pname
        win = Tk()
        win.title('Sudoku')
        Label(win, text='Please provide the following details').pack(pady=30)
        win.geometry('500x400')

        Sname = StringVar()
        Pname = StringVar()

        frame1 = Frame(win)
        name = Entry(frame1, textvariable=Sname)

        label = Label(win, text="Enter Server Address")
        label.pack()
        name.grid(row=0, column=1, sticky=W)

        frame1.pack()
        label2 = Label(win, text="Enter port")
        name1 = Entry(win, textvariable=Pname)
        label2.pack()
        name1.pack()

        # Define a frame
        frame2 = Frame(win, width=200, height=300)

        # Define two buttons and each saved inside the framee
        b1 = Button(frame2, text=" Enter ", command=lambda: save1(Sname, Pname))

        # b1 = Button(frame2, text=" Enter ", command=lambda:sav)

        b4 = Button(frame2, text=" Cancel ", command=lambda: exit(sys))

        # Call the pack function to set the visibility of the buttons true
        b1.pack(side=LEFT, padx=10, pady=10)
        b4.pack(side=RIGHT, padx=10, pady=10)

        frame2.pack()
        return win

    win = makeWindow()
    win.mainloop()


def openclient(player):
    player.get()
    name = player.get()
    execfile('Sudoku_Client.py')
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

'''
The makeWindow() function creates the GUI interface using Tkinter widgets. All widgets are activated or displayed by calling the pack function,
which is a default function for every widget is called.
'''

def makeWindow():
    global nameVar, namSugg
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
    f = open('Player_Name.txt').readlines()
    for word in f:
        item = word
        listbox.insert(END, item)
        listbox.pack(side = LEFT, fill = BOTH)
        scrollbar.config(command = listbox.yview)

    C.pack(pady = 40)
    b = Button(C, text = 'Save Player', command = lambda:save(nameVar))
    b1 = Button(C, text = 'Enter', command = lambda:openServer(nameVar))
    b4 = Button(C, text = 'Cancel', command = lambda:exit(sys))
    b.pack(side = LEFT, padx = 20)
    b1.pack(side = LEFT, padx = 20)
    b4.pack(side = RIGHT, padx = 20)
    frame2.pack()
    return won



# Threads for server discovery over the network
discover = threading.Thread(target=Try_Discovering_Server)
discover.start()

won = makeWindow()
won.mainloop()


