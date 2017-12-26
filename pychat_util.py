import socket, pdb
import future_builtins
import future

MAX_CLIENTS = 30
PORT = 12345
QUIT_STRING = '<$quit$>'

import random
from objects import SudokuSquare
from objects import SudokuGrid
from objects import GameResources


#------------------------------------------------------------------------------------------------

'''
===< Implementing 3-tier structure: Hall --> Room --> Clients for multiplayer Sudoku >====

PyChat Util handles server's complete reception according to the client's
particular requests. Our approach creates different rooms in a Hall. So we have
declared a Hall Class and a Room class for these purpose. Also every player has 
its own properties like name and socket address, So there is a Player class to handle
this information.

Every client is given the liberty to either join an existing room or
create new room in the Hall.

The Client's messages are handled here according to the signature terms
which are currently known by both the client and the server side.

'''

#=============================================================================================

def getSudoku(puzzleNumber=None):
    """This function defines the solution and the inital view.
    Returns two lists of lists, inital first then solution."""

    inital = SudokuGrid.SudokuGrid()
    current = SudokuGrid.SudokuGrid()
    solution = SudokuGrid.SudokuGrid()

    inital.createGrid(27, puzzleNumber)
    current.createGrid(27, puzzleNumber)
    solution.createGrid(81, puzzleNumber)

    return inital, current, solution

def create_socket(address):
    """This function takes the server address and start listening at
    that particular address with corresponding socket.."""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    print "Now listening at ", address
    return s


#=============================================================================================


class Hall:
    """
    The Hall class handles all the messages by client and perform operations accordingly
    i.e create new rooms, iterate through current rooms , show room lists etc.
    """

    def __init__(self):
        self.rooms = {} # {room_name: Room}
        self.room_player_map = {} # {playerName: roomName}



    """
    Initial Reception: Send room list to client side..
    """
    def welcome_new(self, new_player):
        #new_player.socket.sendall(b'Welcome to pychat.\nPlease tell us your name:\n')
        self.list_rooms(new_player)



    """
    List all present rooms.
    """
    def list_rooms(self, player):
        
        if len(self.rooms) == 0:
            msg = 'Oops, no active rooms currently. Create your own!\n' \
                + 'Write room name..\n'
            player.socket.sendall(msg.encode())
        else:
            msg = 'Listing current rooms choose a room as number ...\n'
            for room in self.rooms:
                msg += room + ": " + str(len(self.rooms[room].players)) + " player(s)\n"
            player.socket.sendall(msg.encode())



    """
    The most crucial function that handles every message sent to server,
    Kindly note that every message has a signature term which we use to 
    differentiate the type of request and what to response.
    """
    def handle_msg(self, player, msg):

        #print player.name + " says: " + msg

        if "name:" in msg:
            name = msg.split()[1]
            player.name = name
            print "New connection from:", player.name
            player.socket.sendall('selection')

        elif "session:" in msg:
            same_room = False
            if len(msg.split()) >= 2: # error check
                room_name = msg.split()[1]
                if player.name in self.room_player_map: # switching?
                    if self.room_player_map[player.name] == room_name:
                        player.socket.sendall(b'You are already in room: ' + room_name.encode())
                        same_room = True
                    else: # switch
                        old_room = self.room_player_map[player.name]
                        self.rooms[old_room].remove_player(player)
                if not same_room:
                    if not room_name in self.rooms: # new room:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].players.append(player)
                    self.rooms[room_name].welcome_new(player)

                    self.room_player_map[player.name] = room_name
                    #player.socket.sendall(self.r)
            else:
                print('isnt----------------')
                #player.socket.sendall(instructions)

        elif "<list>" in msg:
            self.list_rooms(player)
        
        elif "<quit>" in msg:
            player.socket.sendall(QUIT_STRING.encode())
            self.remove_player(player)

        elif "u:" in msg:
            coordinate_string = msg.replace("u:", "")
            coordinate_string2=coordinate_string.replace(","," ")
            coordinate_list_int=[]
            coordinate_list_int.append(int(coordinate_string2.split()[0]))
            coordinate_list_int.append(int(coordinate_string2.split()[1]))
            coordinate_list_int.append(int(coordinate_string2.split()[2]))
            for room in self.rooms:
                for newplayer in self.rooms[room].players:
                    if(player is newplayer):
                        self.rooms[room].gameObject.setNum(coordinate_list_int[0], coordinate_list_int[1], coordinate_list_int[2])
                        self.rooms[room].broadcast_grid()
                        break

        elif "refresh:" in msg:
            for room in self.rooms:
                for newplayer in self.rooms[room].players:
                    if (player is newplayer):
                        self.rooms[room].broadcast_grid()
                        break

    """
    The remove player method to remove a particular player from its room
    """
    def remove_player(self, player):
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player)
            del self.room_player_map[player.name]
        print "Player: " + player.name + " has left\n"



#=============================================================================================


class Room:
    """
    The Room class handles creates a new game for every room,
    Welcomes new player and send the grid to new player,
    Broadcast updated grid to all players in current room and
    Removes a player from current room.
    """


    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name
        initial,current,solution = getSudoku()
        self.gameObject = current
        self.grid = current.get_Grid()


    """
    Welcome new player to this and return the corresponding game to the new player.
    """
    def welcome_new(self, from_player):
        i=0
        send_grid=''
        for row in self.grid:
            for col in row:
                send_grid=send_grid+','+str(col)
                i+=1
        msg = "welcomes: " + send_grid
        for player in self.players:
            player.socket.sendall(msg.encode())



    """
    Broadcast Game grid update to every member in current room.
    """
    def broadcast_grid(self):
        i = 0
        send_grid = ''
        for row in self.grid:
            for col in row:
                send_grid = send_grid + ',' + str(col)
                i += 1
        msg = "grid: " + send_grid
        for player in self.players:
            player.socket.sendall(msg)


    """
    Broadcast messages other than grid updates, For Example: 'Player has left'
    """
    def broadcast(self, from_player, msg):
        msg = from_player.name.encode() + b":" + msg
        for player in self.players:
            player.socket.sendall(msg)



    """
    Remove a particular player from this room and broadcast it to other room members
    """
    def remove_player(self, player):
        self.players.remove(player)
        leave_msg = player.name.encode() + b"has left the room\n"
        self.broadcast(player, leave_msg)



#=============================================================================================


class Player:
    """
    The Player class for storing socket information and name of every player
    """

    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

    def fileno(self):
        return self.socket.fileno()
