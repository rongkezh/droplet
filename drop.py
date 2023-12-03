# testing purpose only

# testing direction with board 2d array
import random
pop_size = 9
size = 5
board = [[random.randint(0, pop_size-1) for j in range(size)] for i in range(size)]
def printboard():
    for i in range(size):
        for j in range(size):
            print(f'{board[i][j]} ', end='')
        print()
row = 1
col = 1
index = board[row][col]
printboard()
print(f'{index}')
direction = [-1,0]
rowadd,coladd = direction
print(rowadd)
print(coladd)
index = board[row+rowadd][col+coladd]
print(index)