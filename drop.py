# main class
# TODO: UI
import random
# 
class Game:
    def __init__(self):
        self.gameboard = {}
        msg = "Welcome to droplets game."
        print(msg)
        # game status. False if game is finished.
        self.on = True
    def off(self):
        self.on = False
class Board:
    def __init__(self, length, difficulty):
        self.length = length
        # TODO: difficulty level should affect the map generation.
        self.map = [[random.randint(0,9) for i in range(length)] for j in range(length)]
    def printmap(self):
        for row in self.map:
            for elem in row:
                print(elem, end=' ')
            print()

# drops at grids
class Drop:
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size

    def __str__(self):
        return f"({self.x},{self.y}){self.size}"

    def add_water(self,x,y):
        self.size += 1
        if self.size > 9:
            self.size = 0
            # TODO: splash to four directions; if no drop in any direction, splash would bounce and diminish on the boarder.

