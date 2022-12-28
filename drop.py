# main class

class Game:
    def __init__(self):
        self.gameboard = {}
        msg = "Welcome to droplets game."
        print(msg)
    def main(self):
        while True:
            print("main")
            break


# drops at grids
class Drop:
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size

    def __str__(self):
        return f"({self.x},{self.y}){self.size}"

    def add_water(self):
        self.size += 1
        if self.size > 9:
            self.size = 0
            # TODO: splash to four directions; if no drop in any direction, splash would bounce and diminish on the boarder.

