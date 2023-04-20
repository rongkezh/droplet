from drop import Drop
from drop import Game
import random

# Display a welcome message

# Generate a random map of droplets.


drop1 = Drop(1,2,1)
print(drop1)

# Initialize gridmap
# size of the gridmap = 5
length = 5
gridmap = [[0 for i in range(length)] for j in range(length)]
# Random gridmap generation(TODO)
# difficulty = input("Choose your difficulty level from 1(easiest) to 5(hardest): ")

# gridmap[0][2] = random.randint(0,9)
# using gridmap default for the basics of the game.
gridmapdefault = [[random.randint(0,9) for i in range(length)] for j in range(length)]

# print gridmap function
def printmap(gridmap):
    for row in gridmap:
        for elem in row:
            print(elem, end=' ')
        print()

def adddrop(gridmap, x, y):
    if gridmap[x][y]<1:
        print("You can only add water drop to non-vacant grids.\n Please enter valid coordinates")
        pass
    if gridmap[x][y]>8:
        gridmap[x][y] = 0
        #TODO: simplify the ripple out process of the drop to four directions
        for row in gridmap:
            for elem in row:
                
    else:
        gridmap[x][y] +=1


def gridmapfinished(gridmap):
    if (sum([sum(i) for i in gridmap]) == 0):
        game.off()

# each time, 
game = Game()
while (game.on):
    # TODO: printmap()
    print("The current map:")
    printmap(gridmapdefault)
    print("You have n drops of water left.") # TODO: print the number of water drops left for the player
    print("Please choose the coordinates (x,y) on the you'd like to add water to:")
    x = int(input("Please enter x value:"))
    y = int(input("Please enter y value:"))
    adddrop(gridmapdefault,x,y)
    # TODO: read x, y value of the incoming water drop
    
    gridmapfinished(gridmapdefault)