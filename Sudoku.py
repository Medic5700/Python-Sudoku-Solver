'''
A small program to solve a sudoku puzzle
'''

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

def stringToField(rawInput : str) -> List[List[int or None]]:
     '''Takes in a string representing a sudoku board, and returns a list of lists representing the board.

     Single digit hexadecimal numbers are converted to ints.
     '-' is converted to None

     result[y][x] is the value at position (x,y), origin at top left, x increasing right, y increasing down
     '''
     assert type(rawInput) is str
     assert len(rawInput) >= 81

     field : List[List[int or None]] = [[None for _ in range(9)] for _ in range(9)]

     rawNumbers : List[int or None] = [int(j, base=16) if (j in "0123456789abcdef") else None for j in [i for i in rawInput.lower() if ((i in "0123456789abcdef") or i == "-")]]
     
     assert len(rawNumbers) == 81

     field = [[rawNumbers[i*9 + j] for j in range(9)] for i in range(9)]

     return field

def bitPatternToBrailleSquare(rawInput : List[bool]) -> str:
     '''Takes in a list of booleans representing a braille square, and returns a string representing the square.

     Numbering of the braille squares is as follows:
          0 1 | 2 3
          4 5 | 6 7
          8 9 | a b
          c d | e f
          left|right

     #TODO: add a test for this function
     test with 
          bitPatternToBrailleSquare([True if i == "1" else False for i in "1111111000000000"])
     '''
     assert type(rawInput) is list
     assert len(rawInput) == 16
     assert all(type(i) is bool for i in rawInput)

     leftmap : List[bool] =  (rawInput[0x0], rawInput[0x1], rawInput[0x4], rawInput[0x5],
                              rawInput[0x8], rawInput[0x9], rawInput[0xc], rawInput[0xd])
     rightmap : List[bool] = (rawInput[0x2], rawInput[0x3], rawInput[0x6], rawInput[0x7],
                              rawInput[0xa], rawInput[0xb], rawInput[0xe], rawInput[0xf])

     brailleValueMap : List[int] = [0x01, 0x08, 0x02, 0x10, 0x04, 0x20, 0x40, 0x80] # maps a value to every 'dot' corrisponding to positions '014589cd'

     leftValue : int = 0x2800 + sum([leftmap[i]*brailleValueMap[i] for i in range(8)])
     rightValue : int = 0x2800 + sum([rightmap[i]*brailleValueMap[i] for i in range(8)])

     return chr(leftValue) + chr(rightValue)

def field9x9_toString(field : List[List[int or None]], possible : List[List[List[bool]]] = [[[False for _ in range(16)] for _ in range(9)] for _ in range(9)]) -> str:
     '''Takes in a 9x9 field and returns a string representing the field to be printed to screen.

     also takes in a 'possible' field to represent the pencil possibility space of the field.
     unfilled values in field are represented by a unicode braille characters.

     #TODO: add a test for this function
     use the following test to verify the output
          possible : List[List[List[bool]]] = [[[True if i == "1" else False for i in bin(random.randint(0, 0xffff))[2:].rjust(16, '0')] for _ in range(9)] for _ in range(9)]
     '''
     assert type(field) is list
     assert len(field) == 9
     assert all(type(i) is list for i in field)
     assert all(len(i) == 9 for i in field)
     assert all(all(type(j) is int or j is None for j in i) for i in field)

     assert type(possible) is list
     assert len(possible) == 9
     assert all(type(i) is list for i in possible)
     assert all(len(i) == 9 for i in possible)
     assert all(all(type(j) is list for j in i) for i in possible)
     assert all(all(len(j) == 16 for j in i) for i in possible)
     assert all(all(all(type(k) is bool for k in j) for j in i) for i in possible)

     output : str = ""

     for i in range(9):
          for j in range(9):
               if field[i][j] == None:
                    output += bitPatternToBrailleSquare(possible[i][j])
               else:
                    output += str(field[i][j]).rjust(2)
               if (j%3 == 2) and (j != 8):
                    output += "|"
          output += "\n"
          if (i%3 == 2) and (i != 8):
               output += "------+------+------\n"
     return output

def pencil9x9_singleCell(field : List[List[int or None]], y : int, x : int) -> List[bool]:
     '''Takes in a sudoku board, and returns a list of lists representing the pencil marks for the cell at (i,j).
     '''
     assert type(field) is list
     assert len(field) == 9
     assert all(type(i) is list for i in field)
     assert all(len(i) == 9 for i in field)
     assert all(all(type(j) is int or j is None for j in i) for i in field)

     assert type(y) is int
     assert y in range(9)
     assert type(x) is int
     assert x in range(9)

     possible : List[bool] = [True if i == "1" else False for i in "1111111110000000"]

     for i in range(9): # check row
          if field[y][i] != None:
               value = field[y][i]
               possible[value - 1] = False
     for i in range(9): # check column
          if field[i][x] != None:
               value = field[i][x]
               possible[value - 1] = False
     for i in range(3): # check square
          for j in range(3):
               if field[(y//3)*3 + i][(x//3)*3 + j] != None:
                    value = field[(y//3)*3 + i][(x//3)*3 + j]
                    possible[value - 1] = False

     return possible

def pencil9x9(field : List[List[int or None]]) -> List[List[List[bool]]]:
     '''Takes in a sudoku board, and returns a list of lists representing the pencil marks for all cells.
     '''
     assert type(field) is list
     assert len(field) == 9
     assert all(type(i) is list for i in field)
     assert all(len(i) == 9 for i in field)
     assert all(all(type(j) is int or j is None for j in i) for i in field)

     possible : List[List[List[bool]]] = [[[False for _ in range(16)] for _ in range(9)] for _ in range(9)]

     for i in range(9):
          for j in range(9):
               if field[i][j] == None:
                    possible[i][j] = pencil9x9_singleCell(field, i, j)

     return possible

     '''
     for i in range(9):
          for j in range(9):
     
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


     testField : str
     
     testField = """-7-9-----
                    --3-712--
                    --485--73
                    --1---5-7
                    -465-7381
                    5-71--9-2
                    7---198--
                    --82657--
                    --97-8-2-"""
     # solved
     # 275936418
     # 683471295
     # 194852673
     # 821693547
     # 946527381
     # 537184962
     # 762319854
     # 418265739
     # 359748126
 
     testField = """---74---6
                    4-68--5-7
                    7---9---4
                    -3-9847--
                    82-6134-9
                    -4----3--
                    -6237---5
                    --54-9---
                    -7--612-8"""
     # solved
     # 218745936
     # 496832517
     # 753196824
     # 531974762
     # 827613459
     # 649257381
     # 962378145
     # 185429673
     # 374561298
     
