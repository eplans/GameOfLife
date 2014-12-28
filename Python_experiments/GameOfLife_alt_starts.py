import pygame, sys
from pygame.locals import *
import time
import random

FPS = 30
###Sets size of grid
WINDOWWIDTH = 640
WINDOWHEIGHT = 450
CELLSIZE = 5
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"
CELLWIDTH = WINDOWWIDTH / CELLSIZE # number of cells wide
CELLHEIGHT = WINDOWHEIGHT / CELLSIZE # Number of cells high

# set up the colors
BLACK =    (0,  0,  0)
WHITE =    (255,255,255)
DARKGRAY = (40, 40, 40)
GREEN =    (0,255,0)

#Draws the grid lines
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x,0),(x,WINDOWHEIGHT))
    for y in range (0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0,y), (WINDOWWIDTH, y))

def colourGrid(item, lifeDict):
    x = item[0]
    y = item [1]
    if lifeDict[item] == 0:
        y = y * CELLSIZE # translates array into grid size
        x = x * CELLSIZE # translates array into grid size
        pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, CELLSIZE, CELLSIZE))
    if lifeDict[item] == 1:
        y = y * CELLSIZE # translates array into grid size
        x = x * CELLSIZE # translates array into grid size
        pygame.draw.rect(DISPLAYSURF, GREEN, (x, y, CELLSIZE, CELLSIZE))
    return None

def blankGrid():
    gridDict = {}
    for y in range (CELLHEIGHT):
        for x in range (CELLWIDTH):
            gridDict[x,y] = 0
    return gridDict

def startingGridRandom(lifeDict):
    for item in lifeDict:
        lifeDict[item] = random.randint(0,1)
    return lifeDict

def startingRpentomino(lifeDict):
    #R-pentomino
    lifeDict[48,32] = 1
    lifeDict[49,32] = 1
    lifeDict[47,33] = 1
    lifeDict[48,33] = 1
    lifeDict[48,34] = 1
    return lifeDict


def startingAcorn(lifeDict):
    #Acorn
    lifeDict[105,55] = 1
    lifeDict[106,55] = 1
    lifeDict[109,55] = 1
    lifeDict[110,55] = 1
    lifeDict[111,55] = 1
    lifeDict[106,53] = 1
    lifeDict[108,54] = 1
    return lifeDict

def startingDiehard(lifeDict):
    #Diehard
    lifeDict[45,45] = 1
    lifeDict[46,45] = 1
    lifeDict[46,46] = 1
    lifeDict[50,46] = 1
    lifeDict[51,46] = 1
    lifeDict[52,46] = 1
    lifeDict[51,44] = 1
    return lifeDict

def startingGosperGliderGun(lifeDict):
    #Gosper Glider Gun
    #left square
    lifeDict[5,15] = 1
    lifeDict[5,16] = 1
    lifeDict[6,15] = 1
    lifeDict[6,16] = 1
    #left part of gun
    lifeDict[15,15] = 1
    lifeDict[15,16] = 1
    lifeDict[15,17] = 1
    lifeDict[16,14] = 1
    lifeDict[16,18] = 1
    lifeDict[17,13] = 1
    lifeDict[18,13] = 1
    lifeDict[17,19] = 1
    lifeDict[18,19] = 1
    lifeDict[19,16] = 1
    lifeDict[20,14] = 1
    lifeDict[20,18] = 1
    lifeDict[21,15] = 1
    lifeDict[21,16] = 1
    lifeDict[21,17] = 1
    lifeDict[22,16] = 1
    #right part of gun
    lifeDict[25,13] = 1
    lifeDict[25,14] = 1
    lifeDict[25,15] = 1
    lifeDict[26,13] = 1
    lifeDict[26,14] = 1
    lifeDict[26,15] = 1
    lifeDict[27,12] = 1
    lifeDict[27,16] = 1
    lifeDict[29,11] = 1
    lifeDict[29,12] = 1
    lifeDict[29,16] = 1
    lifeDict[29,17] = 1
    #right square
    lifeDict[39,13] = 1
    lifeDict[39,14] = 1
    lifeDict[40,13] = 1
    lifeDict[40,14] = 1
    return lifeDict
    
def getNeighbours(item,lifeDict):
    neighbours = 0
    for x in range (-1,2):
        for y in range (-1,2):
            checkCell = (item[0]+x,item[1]+y)
            if checkCell[0] < CELLWIDTH  and checkCell[0] >=0:
                if checkCell [1] < CELLHEIGHT and checkCell[1]>= 0:
                    if lifeDict[checkCell] == 1:
                        if x == 0 and y == 0: # negate the central cell
                            neighbours += 0
                        else:
                            neighbours += 1
    return neighbours

def tick(lifeDict):
    newTick = {}
    for item in lifeDict:
        #get number of neighbours
        numberNeighbours = getNeighbours(item, lifeDict)
        if lifeDict[item] == 1: # For those cells already alive
            if numberNeighbours < 2: # kill underpopulation
                newTick[item] = 0
            elif numberNeighbours > 3: # kill over population
                newTick[item] = 0
            else:
                newTick[item] = 1 # keep status quo
        elif lifeDict[item] == 0:
            if numberNeighbours == 3: # cell reproduces
                newTick[item] = 1
            else:
                newTick[item] = 0 # keep status quo
    return newTick

def main():
    pygame.init()
    global DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Game of Life')

    DISPLAYSURF.fill(WHITE)

    lifeDict = blankGrid() # creates library and Populates to match blank grid

    ###Starting options
    #lifeDict = startingGridRandom(lifeDict) # Assign random life
    lifeDict = startingRpentomino(lifeDict) # Setup R-pentomino
    #lifeDict = startingAcorn(lifeDict) # Setup Acorn
    #lifeDict = startingDiehard(lifeDict)
    #lifeDict = startingGosperGliderGun(lifeDict)

    #Colours the live cells, blanks the dead
    for item in lifeDict:
        colourGrid(item, lifeDict)

    drawGrid()
    pygame.display.update()
        
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #runs a tick
        lifeDict = tick(lifeDict)

        #Colours the live cells, blanks the dead
        for item in lifeDict:
            colourGrid(item, lifeDict)

        drawGrid()
        pygame.display.update()    
        FPSCLOCK.tick(FPS)
if __name__=='__main__':
    main()
