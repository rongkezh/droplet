import random

class Board:
    def __init__(self, size, pop_size):
        self.size = size
        self.pop_size = pop_size
        self.board = [[random.randint(0, pop_size-1) for j in range(size)] for i in range(size)]
    
    def print_board(self):
        for i in range(self.size):
            for j in range(self.size):
                print(f'{self.board[i][j]} ', end='')
            print()
    
    def add_water(self, row, col, amount):
        if self.board[row][col] + amount > self.pop_size:
            overflow = self.board[row][col] + amount - self.pop_size
            self.board[row][col] = self.pop_size
            self.pop(row, col)
            return overflow
        else:
            self.board[row][col] += amount
            return 0
    
    def pop(self, row, col):
        drops = self.board[row][col] - 1
        self.board[row][col] = 0
        for r, c in [(row-1,col), (row+1,col), (row,col-1), (row,col+1)]:
            if r >= 0 and r < self.size and c >= 0 and c < self.size:
                if self.board[r][c] > 0:
                    self.board[r][c] += 1
                else:
                    self.board[r][c] = 1
                    self.splash(r, c, drops)
    
    def splash(self, row, col, drops):
        if drops <= 0:
            return
        for r, c in [(row-1,col), (row+1,col), (row,col-1), (row,col+1)]:
            if r >= 0 and r < self.size and c >= 0 and c < self.size:
                if self.board[r][c] > 0:
                    self.board[r][c] += 1
                else:
                    self.board[r][c] = 1
                    self.splash(r, c, drops-1)


class Game:
    def __init__(self, size=5, pop_size=3, water=100):
        self.board = Board(size, pop_size)
        self.water = water
        self.rounds = 0
    
    def play(self):
        while self.water > 0:
            self.board.print_board()
            print(f'You have {self.water} drops of water.')
            row = int(input('Enter row: '))
            col = int(input('Enter col: '))
            amount = 1
            overflow = self.board.add_water(row, col, amount)
            self.water -= amount - overflow
            self.rounds += 1
            if self.check_win():
                print('You win!')
                return
        print('You lose!')
    
    def check_win(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] > 0:
                    return False
        return True


if __name__ == '__main__':
    game = Game()
    game.play()
