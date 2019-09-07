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

if __name__ == "__main__":
     Board = [[0 for i in range(9)] for j in range(9)]
     
     #Gets the puzzle from the user to solve
     for i in range(9):
          raw = input("input puzzle line " + str(i+1) + ":")
          raw = raw.ljust(9," ")
          for j in range(9):
               if raw[j] in ("1","2","3","4","5","6","7","8","9"):
                    Board[i][j] = int(raw[j])
                    
     printBoardSimple(Board)
     
     for i in range(9):
          for j in range(9):
               Board[i][j] = pencil(Board, i,j)     
     
     printBoard()

