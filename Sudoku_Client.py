from __future__ import print_function

import sys, os
import pygame               # Must install pygame for this module to work (see Manual)
sys.path.append(os.path.join("objects"))
sys.path.append(os.path.join("Server Side"))
sys.path.append(os.path.join("Client Side"))
from GameResources import *
import Client_Handler
import select, socket, sys
import pychat_util
import threading
import time


#-----------------------------------------------------------------

'''
Sudoku Client script handles the initial server connection 
and resolves the protocols. When the client is assigned a room
and a game this script runs two threads:

1- For continous reception of Grid Updation from server
2- Game Logic and GUI of Client Handler
'''

###############################################################################

from Tkinter import *
import tkMessageBox as messagebox
import Tkinter as tk
import sys
#import Sudoku_Client

'''
This is the user interface code for Sudoku GUI. It asks for a player name first and saves the player name
in a txt file. If a player has already saved his/her name, the player can select his/her name from a listbox appearing
in the main window.
'''

UserName=''
Sname=''
Pname=''
Inputs_Done=False

def create_window():

    window = tk.Toplevel()

'''
The openServer functions executes, when the player name is accepted. It opens a new python window where the player need to specify
the server address and port number.
'''
def openServer(player):

    global UserName
    UserName = player.get()
    UserName = player.get()
    print(UserName)



    '''
    The create_window() function creates a window.
    '''

    def create_window():
        window = tk.Toplevel()

    def save1(sname, pname):
        global Inputs_Done
        global won
        Inputs_Done=True
        win.destroy()
        won.destroy()

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





won = makeWindow()
won.mainloop()



##################################################################################

READ_BUFFER = 4096
score=0
server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_connection.connect(('127.0.0.1', pychat_util.PORT))



"""
A recursive method running under reception thread
to recive continous updated grid from server.
"""

def refresh_query():
    time.sleep(1)
    msg='refresh:'
    try:
        server_connection.sendall(msg.encode())
        msg = server_connection.recv(READ_BUFFER)
        self_grid = msg.replace("grid: ", "")
        grid = []
        li = []
        string_grid = self_grid.split(',')
        for element in string_grid:

            # print(element.strip())
            element = element.strip()
            if (element.strip() == 'None'):
                li.append(None)
            elif (len(element.strip()) > 0):
                li.append(int(element))
                # li.append(1)

            if (len(li) == 9):
                grid.append(list(li))
                li = []

        for i in range(9):
            for j in range(9):
                if(Client_Handler.MainGrid[i][j] is not grid[i][j]):
                    print("Old = ",Client_Handler.MainGrid[i][j])
                    print("New = ",grid[i][j])
                    x= 9*(i)
                    y= x+j
                    Client_Handler.theSquares[y].change(grid[i][j])
                    print('i  and j = ',i,j)
                    print('location = %d'%y)
                    print('number = ',grid[i][j])
        Client_Handler.MainGrid = grid
    except:
        print('')


    refresh_query()


#------------------------------------------------------------------------------------------------------


def prompt():
    print('>', end=" ")



print ("Connected to server\n")
msg_prefix = ''                                 # msg prefix is appended as signature term for server
socket_list = [sys.stdin, server_connection]
name=UserName


"""
Initial connection and protocol resolution from client side
is handled in this loop
"""
while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if(Inputs_Done):
            if s is server_connection: # incoming message
                msg = s.recv(READ_BUFFER)
                if not msg:
                    print ("Server down!")
                    sys.exit(2)
                else:
                    if msg == pychat_util.QUIT_STRING.encode():
                        sys.stdout.write('Bye\n')
                        sys.exit(2)
                    else:
                        sys.stdout.write(msg.decode())
                        if 'Listing current rooms' in msg.decode():
                            msg_prefix = 'name: '+name  # Send user name to server
                            server_connection.sendall(msg_prefix.encode())
                            continue

                        elif 'Oops' in msg.decode():
                            msg_prefix = 'name: ' + name  # Send user name to server
                            server_connection.sendall(msg_prefix.encode())
                            continue

                        elif 'welcomes' in msg.decode() and Client_Handler.inroom is False:
                            #print('WElcome...')
                            grid=msg.replace("welcomes: ", "")      # replace signature term with empty and
                            handle = Client_Handler.Handler()       # Client Handler Handle class object

                            # Threads to operate client's reception and game GUI
                            game = threading.Thread(target=handle.Initial_Reception, args=(grid,name,s))
                            refreshloop = threading.Thread(target=refresh_query)
                            game.start()
                            refreshloop.start()
                            game.join()
                            refreshloop.join()

                            Client_Handler.inroom=True

                        elif 'selection' in msg.decode():

                            msg_prefix = 'session: '  # identifier for new session

                        elif 'grid: ' in msg:

                            grid = msg.replace("grid: ", "") # identifier for grid

                        else:
                            msg_prefix = ''

                        if(Client_Handler.inroom is False):
                            prompt()

            else:
                #print(Client_Handler.inroom)
                if(Client_Handler.inroom is False):

                    #print('Waiting for client input...')
                    msg = msg_prefix + sys.stdin.readline()
                    server_connection.sendall(msg.encode())
