import socket, pdb
import future_builtins
import future

import random
from objects import SudokuSquare
from objects import SudokuGrid
from objects import GameResources


#------------------------------------------------------------------------------------------------

'''
===< Implementing 3-tier structure: Hall --> Room --> Clients for multiplayer Sudoku >====

PyChat Util handles server's complete reception according to the client's
particular requests. Our approach creates different rooms in a Hall. So we have
declared a Hall Class and a Room class for these purpose.

Every client is given the liberty to either join an existing room or
create new room in the Hall.

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

#=============================================================================================


class Hall:
    """
    The Hall class handles all the RPC calls by client and perform operations accordingly
    i.e create new rooms, iterate through current rooms , show room lists etc.
    """

    def __init__(self):
        self.rooms = {} # {room_name: Room}
        self.room_names=[]
        self.room_player_map = {} # {playerID: roomName}

    """
    Initial Reception: Send room list to client side..
    """
    def Welcome_and_getList(self, new_player, player_id):
        return self.list_rooms()

    """
        returns a Tuple (True and roomnames) if room_names is not empty
                      (false and None) if room_names is empty 
    """
    def list_rooms(self):
        if len(self.rooms) == 0:
           return False, None
        else:
            return True, self.room_names

    """
        Create new room with player name for CLient and return the Sudoku Grid
    """
    def create_room(self,new_player, room_name):
        new_room = Room(room_name)
        self.room_names.append(room_name)
        self.rooms[room_name] = new_room
        self.room_player_map[new_player]=room_name
        self.rooms[room_name].players.append(new_player)
        return self.rooms[room_name].Update_Grid()

    """
        Join an already existing room and return the perspective room's Sudoku Grid
    """
    def join_room(self,new_player, room_name):

        self.room_player_map[new_player] = room_name
        self.rooms[room_name].players.append(new_player)
        return self.rooms[room_name].Update_Grid()

    """
        Return Grid by Room name
    """
    def Get_Grid(self,room_name):
        return self.rooms[room_name].Update_Grid()

    """
        Update values of a room's grid
    """
    def update_index_value(self,msg,room):
        coordinate_string = msg.replace("u:", "")
        coordinate_string2 = coordinate_string.replace(",", " ")
        coordinate_list_int = []
        coordinate_list_int.append(int(coordinate_string2.split()[0]))
        coordinate_list_int.append(int(coordinate_string2.split()[1]))
        coordinate_list_int.append(int(coordinate_string2.split()[2]))

        self.rooms[room].gameObject.setNum(coordinate_list_int[0], coordinate_list_int[1],
                                                       coordinate_list_int[2])
        return None

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
    """


    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name
        initial,current,solution = getSudoku()
        self.gameObject = current
        self.grid = current.get_Grid()

    """
        Returns current updated grid to Hall's Request
    """
    def Update_Grid(self):
        return self.grid

    """
    Remove a particular player from this room and broadcast it to other room members
    """
    def remove_player(self, player):
        self.players.remove(player)
        leave_msg = player.name.encode() + b"has left the room\n"
        self.broadcast(player, leave_msg)



#=============================================================================================
