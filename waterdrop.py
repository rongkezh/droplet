import random

class Board:
    def __init__(self, size, pop_size):
        # size is the number of spaces per row or per col.
        # pop_size is the max for a water cell. when pop_size =  3, if a cell is larger than 3, it pops

        self.size = size
        self.pop_size = pop_size
        # randomize the board of cells.
        self.board = [[random.randint(0, pop_size-1) for j in range(size)] for i in range(size)]
    
    def print_board(self):
        for i in range(self.size):
            for j in range(self.size):
                print(f'{self.board[i][j]} ', end='')
            print()
    
    def add_water(self, row, col):
        # add drop to cell at row,col. TODO:return the overflow of drops
        self.board[row][col] += 1
        if self.board[row][col]>= self.pop_size:
            #overflow = self.board[row][col] - self.pop_size
            self.pop(row, col)
            #return overflow
            return
        else:
            return
    
    def pop(self, row, col):
        self.board[row][col] = 0
        #TODO: make water travel in four directions.
        #for direction in ((row-1,col), (row+1,col), (row,col-1), (row,col+1)):
        # cells at up, down, left, right, add_water.
        for r,c in [(-1,0), (+1,0), (0,-1), (0,+1)]:
            # check if out of bounds
            row1=row+r
            col1=col+c
            if (row1) >= 0 and (row1) < self.size and (col1) >= 0 and (col1) < self.size:
                if self.board[row1][col1] > 0:
                    self.add_water(row1,col1)
                else:
                    self.splash(row1, col1, r, c)
    def splash(self, row, col, r, c):
        row1=row+r
        col1=col+c
        if (row1) >= 0 and (row1) < self.size and (col1) >= 0 and (col1) < self.size:
            # check if out of bounds
            if self.board[row1][col1] > 0:
                self.add_water(row1,col1)
            else:
                self.splash(row1, col1, r, c)            

class Game:
    def __init__(self, size=5, pop_size=5, water=100):
        # water is the number of drops player has in the game
        self.board = Board(size, pop_size)
        self.water = water
        self.rounds = 0
        self.size = size
        print("Welcom to Droplet game!")
        print(f"On this {size} by {size} board, each cell can hold up to {pop_size} drops of water before it pops.")
        print("Try to pop every cell. Good luck!")
        print(f"You start with {water} number of drops.")
    
    def play(self):
        while self.water > 0:
            self.board.print_board()
            print(f'You have {self.water} drops of water.')
            print('Please enter where to place your next drop of water.')
            # take the row and col numbers and raise exception if not entered in valid form
            row = self.get_input('row')
            col = self.get_input('col')
            overflow = self.board.add_water(row, col)
            # TODO: add overflow to self.water number
            # self.water -= 1- overflow
            self.rounds += 1
            self.water -= 1
            if self.check_win():
                print(f'You win! Total rounds: {self.rounds}')
                return
        print(f'You lose! Total rounds: {self.rounds}')

    def get_input(self,prompt):
        while True:
            print('Enter', prompt,':', end = " ")
            try:
                index = int(input())-1
            except ValueError:
                print(f"Please enter a integer between 1 and {self.size}")
                continue
            if index < 0 or index >= self.size:
                print(f"Please enter a integer between 1 and {self.size}")
                continue
            else:
                break
        return index

    
    def check_win(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] > 0:
                    return False
        return True


if __name__ == '__main__':
    game = Game()
    game.play()

