import os
import select
import sys

sys.path.append(os.path.join("objects"))
from pychat_util import Hall, Player
import pychat_util

#--------------------------------------------------------------------------------------------------------

'''
The Game Server handles the main server side protocol of the game
whenever a client communicates with server, the perspective information
about the client is passed to the Hall to let it process accordingly.
'''


READ_BUFFER = 4096

host = '127.0.0.1'                  # Host address
listen_sock = pychat_util.create_socket((host, pychat_util.PORT))

hall = Hall()           # Session Manager for game rooms
connection_list = []
connection_list.append(listen_sock)

while True:

    read_players, write_players, error_sockets = select.select(connection_list, [], [])
    #print("Waiting for Connections")
    for player in read_players:
        if player is listen_sock: # new connection, player is a socket
            new_socket, add = player.accept()
            new_player = Player(new_socket)
            connection_list.append(new_player)
            hall.welcome_new(new_player)        # Welcome new client

        else: # new message, old client
            msg = player.socket.recv(READ_BUFFER)
            if msg:
                msg = msg.decode().lower()
                hall.handle_msg(player, msg)   # Handle old clients messages
            else:
                player.socket.close()
                connection_list.remove(player)

    for sock in error_sockets: # close error sockets
        sock.close()
        connection_list.remove(sock)



