from tkinter import *
import tkinter.messagebox
from tkinter import font  as tkfont

from xmlrpclib import ServerProxy

###############################################################################

selected_room=None
join=False
proxy=None


###############################################################################

'''
    This method takes in a string name and roomlist and verifies if that
    name already exists in the roomlist or not.
'''

def check_ifExist(roomname,roomlist,wen):
    global selected_room
    global join
    RoomName = roomname

    if not roomname:
        tkinter.messagebox.showinfo("error", "Please Enter a valid name")
        return

    if(roomlist is not None):
        if RoomName in roomlist:
             tkinter.messagebox.showinfo("error", "Room name already exists")
        else:
            selected_room=RoomName
            wen.destroy()
    else:
        selected_room = RoomName
        join=False
        wen.destroy()       # Destroy this GUI window



'''
    Main method of RoomGui that shows already created rooms and
    also gives option to create a new room. If room already exist it shows error
    message to change the name.
'''

def main(server_ip,server_port,username):

    global proxy
    global join

    server = (server_ip, server_port)

    try:
        proxy = ServerProxy("http://%s:%d" % server)
    except KeyboardInterrupt:
        #LOG.warn('Ctrl+C issued, terminating')
        exit(0)
    except Exception as e:
        #LOG.error('Communication error %s ' % str(e))
        exit(1)
    check, data = proxy.Welcome_and_getList(username, 23212)


    master = Tk()
    master.geometry("500x400")
    master.title("Room Selection")
    Label(master, text="Create Room").grid(row=0)

    roomname=StringVar()
    e1 = Entry(master, textvariable=roomname)
    # e1.insert(10, "")

    e1.grid(row=0, column=1)


    Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
    Button(master, text='Enter', command=lambda: check_ifExist((e1.get()),data,master)).grid(row=3, column=1, sticky=W, pady=4)


    def onRoomSelection(roomname,wen):
        global selected_room
        global join

        wen.destroy()
        join =True
        selected_room=roomname

    Label(master, text="Click on Rooms available below to Join:").grid(row=4)
    if(data is not None):
        for i in range(len(data)):
            Button(master, text=data[i], command=lambda: onRoomSelection(data[i],master)).grid(row=i+5, column=1,
                                                                                                 sticky=W, pady=4)

    mainloop()

