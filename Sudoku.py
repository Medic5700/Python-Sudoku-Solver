'''
A small program to solve a sudoku puzzle
'''

def printBoardSimple(Board):
     ''' Takes in the game board, and prints a simple represention (without pencil
     '''
     for i in range(9):
          t1 = ""
          for j in range(9):
               if Board[i][j] == 0:
                    t1 += " "
               elif type(Board[i][j]) != type([]):
                    t1 += str(Board[i][j])
               else:
                    t1 += " "
               if (j%3 == 2) and (j != 8):
                    t1 += "|"
          print(t1)
          print("---+---+---") if (i%3 == 2) and (i != 8) else None

def pencil(Board, r, c):
     '''Takes in the game board, a row number, a column number. Returns an array representing the pencil for the tile
     
     Note: can be used to verify a completed game board. for each game tile, will return a single element list containing the number for that tile.
     '''
     import math
     #pencil in board at position
     if Board[r][c] != 0:
          return Board[r][c]
     possible = [1,2,3,4,5,6,7,8,9]
     for x in range(9): #checks the row
          if Board[x][c] in possible:
               possible.remove(Board[x][c])
     for y in range(9): #checks the column
          if Board[r][y] in possible:
               possible.remove(Board[r][y])
               
     #find the top left position of a 3x3 tile
     tRow = math.floor(r/3)*3
     tColumn = math.floor(c/3)*3
     
     for x in range(3):
          for y in range(3):
               if Board[tRow + x][tColumn + y] in possible:
                    possible.remove(Board[tRow + x][tColumn + y])
     
     return possible

def printBoard():
     line = ""
     for i in range(9): #board row
          for j in range(3): #board subrow
               line = ""
               for k in range(9): #column
                    for l in range(3): #subcolumn
                         #line += str(j*3 + l)
                         if type(Board[i][k]) == type([]):
                              if j*3+l+1 in Board[i][k]:
                                   line += str(j*3+l+1)
                              else:
                                   line += " "
                         else:
                              line += " "
                    if (k==2) or (k==5):
                         line += "::"
                    else:
                         line += "  "
               print(line)
          if (i==2) or (i==5):
               print("=============++=============++=============")
          else:
               print("             ::             ::             ")

def solveBoard(Board, recursionLevel = 0):
     '''Takes in the game board and tries to solve it, returns the solved game board or None of falure
     
     Takes in the game board and tries to solve it, along with the recursion level.
     Recurses when it has to take a guess.
     returns the game board on success, None on failure.
     '''
     
     pass

# typing, for documentation purposes
from typing import Any, Callable, Dict, Generic, List, Literal, Text, Tuple
from copy import deepcopy

     
     '''
     '''
     for i in range(9):
          for j in range(9):
     '''
     
     for i in range(9):
          for j in range(9):

if __name__ == "__main__":
     
     # Board = [[0 for i in range(9)] for j in range(9)]
     # ''' Acceptable board values
     # 1-9   = filled in board tile
     # 0     = empty board tile to be penciled
     # [1-9] = a tile with multiple penciled in values
     # []    = a tile with no filled value and no possible penciled value, an error somewhere else on the board
     # '''
     # '''
     # #Gets the puzzle from the user to solve
     # for i in range(9):
     #      raw = input("input puzzle line " + str(i+1) + ":")
     #      raw = raw.ljust(9," ")
     #      for j in range(9):
     #           if raw[j] in ("1","2","3","4","5","6","7","8","9"):
     #                Board[i][j] = int(raw[j])
     # '''
     # #a debug board configuration
     # Board = [[0,7,0,9,0,0,0,0,0],
     #          [0,0,3,0,7,1,2,0,0],
     #          [0,0,4,8,5,0,0,7,3],
     #          [0,0,1,0,0,0,5,0,7],
     #          [0,4,6,5,0,7,3,8,1],
     #          [5,0,7,1,0,0,9,0,2],
     #          [7,0,0,0,1,9,8,0,0],
     #          [0,0,8,2,6,5,7,0,0],
     #          [0,0,9,7,0,8,0,2,0]]
                    
     # printBoardSimple(Board)
     
     # for i in range(9):
     #      for j in range(9):
     #           Board[i][j] = pencil(Board, i,j)     
     
     # printBoard()

