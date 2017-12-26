import SudokuSquare             # Must install pygame for this module to work (see Manual)
import SudokuGrid               # Must install pygame for this module to work (see Manual)
from GameResources import *     # Must install pygame for this module to work (see Manual)
import sys


'''
The Client Handler script handles all the core client events
i.e Game GUI, Grid updation and modification according to the
data sent by the server. 
'''



"""Global Instances for game GUI and Grid matrix"""
current=None
inroom=False
MainGrid=[]
theSquares = []
pygame.init()
size = width, height = 400, 500
screen = pygame.display.set_mode(size)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))
board, boardRect = load_image("SudokuBg.png")
boardRect = boardRect.move(10, 80)


class Handler:
    """A class to handle server send and recieve data"""

    """Update Grid of the Client Side at the start of the game.."""
    def Update_Grid(self, grid):

        global current
        current = SudokuGrid.SudokuGrid()

        current.set_Grid(grid)

        return current

    """Modify Grid of the Client Side at the start of the game when player joins the room.."""
    def Modify_Grid(self,yLoc, xLoc,event):

        global current
        current.setNum(yLoc, xLoc, event)
        current.printGrid()

        return current

    """Modify Grid of the Client Side if user changes the value of a cell.."""
    def Initial_Reception(self,self_grid,name,s):

        print(".....")
        grid = []
        li = []
        string_grid = self_grid.split(',')
        for element in string_grid:

            #print(element.strip())
            element = element.strip()
            if (element.strip() == 'None'):
                li.append(None)
            elif (len(element.strip()) > 0):
                li.append(int(element))
                # li.append(1)

            if (len(li) == 9):
                grid.append(list(li))
                li = []

        global MainGrid
        MainGrid = grid

        Start(MainGrid,name,s)


    """Send Key Update to the server side upon keydown even by user on client grid.."""
    def Send_Key_Update(self,x,y,number,s):

        coordinate='u:'+str(x)+','+str(y)+','+str(number)
        s.sendall(coordinate)



#------------------------------------------------------



"""Initialize the game GUI and Grid sent from the server..."""

def Start(grid,name,s):
    global background
    global screen
    global size
    global board
    global boardRect
    global theSquares

    handle = Handler()

    # theSquares = []
    initXLoc = 10
    initYLoc = 80
    startX, startY, editable, number = 0, 0, "N", 0
    for y in range(9):
        for x in range(9):
            if x in (0, 1, 2):  startX = (x * 41) + (initXLoc + 2)
            if x in (3, 4, 5):  startX = (x * 41) + (initXLoc + 6)
            if x in (6, 7, 8):  startX = (x * 41) + (initXLoc + 10)
            if y in (0, 1, 2):  startY = (y * 41) + (initYLoc + 2)
            if y in (3, 4, 5):  startY = (y * 41) + (initYLoc + 6)
            if y in (6, 7, 8):  startY = (y * 41) + (initYLoc + 10)
            number = handle.Update_Grid(grid).getNum(y, x)
            if number != None:
                editable = "N"
            else:
                editable = "Y"
            theSquares.append(SudokuSquare.SudokuSquare(number, startX, startY, editable, x, y))

    currentHighlight = theSquares[0]
    currentHighlight.highlight()

    screen.blit(background, (0, 0))
    screen.blit(board, boardRect)
    # screen.blit(logo, logoRect)
    pygame.display.flip()
    pygame.display.set_caption(name)

    theNumbers = {pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2",
                  pygame.K_3: "3", pygame.K_4: "4", pygame.K_5: "5",
                  pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8",
                  pygame.K_9: "9", pygame.K_SPACE: "", pygame.K_BACKSPACE: "",
                  pygame.K_DELETE: ""}

    '''
    Continues Loop for Game Events from keyboards and handling
    '''
    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                for x in theSquares:
                    if x.checkCollide(mousepos):
                        currentHighlight.unhighlight()
                        currentHighlight = x
                        currentHighlight.highlight()
            if event.type == pygame.KEYDOWN and event.key in theNumbers:
                currentHighlight.change(theNumbers[event.key])
                print "[ %s, %s ]" % currentHighlight.currentLoc()
                xLoc, yLoc = currentHighlight.currentLoc()
                handle.Modify_Grid(yLoc, xLoc, theNumbers[event.key])
                handle.Send_Key_Update(yLoc, xLoc, theNumbers[event.key],s)
                current.setNum(yLoc, xLoc, theNumbers[event.key])
                # current.printGrid()

        for num in theSquares:
            num.draw()
        pygame.display.flip()

    exit(sys)
