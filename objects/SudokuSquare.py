import pygame       # Must install pygame for this module to work (see Manual)



class SudokuSquare:
    """A sudoku square class handles all the operation on square,
    For Example : Checking collision and drawing a square on the
    GUI window etc.
    """

    def __init__(self, number=None, offsetX=0, offsetY=0, edit="Y", xLoc=0, yLoc=0):
        if number != None:
            number = str(number)
        else:
            number = ""
        
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(number, 1, (0, 0, 0))
        self.textpos = self.text.get_rect()
        self.textpos = self.textpos.move(offsetX + 12, offsetY + 6)

        self.collide = pygame.Surface((40, 40))
        self.collide = self.collide.convert()
        self.collide.fill((255, 255, 255, 255))
        self.collideRect = self.collide.get_rect()
        self.collideRect = self.collideRect.move(offsetX + 1, offsetY + 1)
        # The rect around the text is 11 x 28

        self.edit = edit
        self.xLoc = xLoc
        self.yLoc = yLoc



    '''
    Draw the square on GUI
    '''
    def draw(self):
        screen = pygame.display.get_surface()
        screen.blit(self.collide, self.collideRect)
        screen.blit(self.text, self.textpos)



    '''
    Check if the the mouse is colliding with current square on GUI
    '''
    def checkCollide(self, collision):
        if len(collision) == 2:
            return self.collideRect.collidepoint(collision)
        elif len(collision) == 4:
            return self.collideRect.colliderect(collision)
        else:
            return False

    '''
    Highlight a square on GUI
    '''
    def highlight(self):
        self.collide.fill((190, 190, 255))
        self.draw()

    '''
    Unhighlight a square on GUI
    '''
    def unhighlight(self):
        self.collide.fill((255, 255, 255, 255))
        self.draw()


    '''
    Change the value of current square on GUI
    '''
    def change(self, number):
        if number != None:
            number = str(number)
        else:
            number = ""
        
        if self.edit == "Y":
            self.text = self.font.render(number, 1, (0, 0, 0))
            self.draw()
            return 0
        else:
            return 1


    '''
    Returns a tuple of current X and Y location of square in the Grid on GUI
    '''
    def currentLoc(self):
        return self.xLoc, self.yLoc