'''
A small program to solve a sudoku puzzle

By Medic5700
'''

from typing import List
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

     # filters out all non-(hexadecimal and '-') characters, and converts them to ints
     rawNumbers : List[int or None] = [int(j, base=16) if (j in "0123456789abcdef") else None for j in [i for i in rawInput.lower() if ((i in "0123456789abcdef") or i == "-")]]
     
     assert len(rawNumbers) == 81 # asserts there is enough data to fill in the board

     field = [[rawNumbers[i*9 + j] for j in range(9)] for i in range(9)] # fills in the board

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

     # maps specific elements of rawInput to specific dots of the braille characters
     leftmap : List[bool] =  (rawInput[0x0], rawInput[0x1], rawInput[0x4], rawInput[0x5],
                              rawInput[0x8], rawInput[0x9], rawInput[0xc], rawInput[0xd])
     rightmap : List[bool] = (rawInput[0x2], rawInput[0x3], rawInput[0x6], rawInput[0x7],
                              rawInput[0xa], rawInput[0xb], rawInput[0xe], rawInput[0xf])

     brailleValueMap : List[int] = [0x01, 0x08, 0x02, 0x10, 0x04, 0x20, 0x40, 0x80] # maps a value to every 'dot' corrisponding to positions '014589cd'

     leftValue : int = 0x2800 + sum([leftmap[i]*brailleValueMap[i] for i in range(8)])
     rightValue : int = 0x2800 + sum([rightmap[i]*brailleValueMap[i] for i in range(8)])
     # 0x2800 is the base braille character (blank braille character)

     return chr(leftValue) + chr(rightValue)

def field9x9_toString(field : List[List[int or None]], possible : List[List[List[bool]]] = None) -> str:
     '''Takes in a 9x9 field and returns a string representing the field to be printed to screen.

     also takes in an optional 'possible' field to represent the pencil possibility space of the field.
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

     if possible is None: # this being here instead of as default variable avoids issue of possible being bound to complex object (and every subsequent call being bound to the same object)
          possible = [[[False for _ in range(16)] for _ in range(9)] for _ in range(9)]
     assert type(possible) is list
     assert len(possible) == 9
     assert all(type(i) is list for i in possible)
     assert all(len(i) == 9 for i in possible)
     assert all(all(type(j) is list for j in i) for i in possible)
     assert all(all(len(j) == 16 for j in i) for i in possible)
     assert all(all(all(type(k) is bool for k in j) for j in i) for i in possible)

     output : str = ""

     i : int
     for i in range(9):
          j : int
          for j in range(9):
               if field[i][j] is None:
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

     i : int
     for i in range(9): # check row
          if field[y][i] != None:
               value = field[y][i]
               possible[value - 1] = False
     i : int
     for i in range(9): # check column
          if field[i][x] != None:
               value = field[i][x]
               possible[value - 1] = False
     i : int
     for i in range(3): # check square
          j : int
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

     i : int
     for i in range(9):
          j : int
          for j in range(9):
               if field[i][j] is None:
                    possible[i][j] = pencil9x9_singleCell(field, i, j)

     return possible

def solveSudoku(field : List[List[int or None]]) -> List[List[int or None]] or None:
     '''Takes in a sudoku board, and returns a list of lists representing the solved board. Returns None if no solution exists.
     '''
     assert type(field) is list
     assert len(field) == 9
     assert all(type(i) is list for i in field)
     assert all(len(i) == 9 for i in field)
     assert all(all(type(j) is int or j is None for j in i) for i in field)

     possible : List[List[List[bool]]]

     newField : List[List[int or None]] = deepcopy(field)
     change : bool = True

     while change:
          change = False
          possible = pencil9x9(newField)

          # fills in any cells that have only one possible value
          i : int
          for i in range(9):
               j : int
               for j in range(9):
                    if newField[i][j] is None:
                         if sum(possible[i][j]) == 1:
                              newField[i][j] = possible[i][j].index(True) + 1
                              change = True
                              break
                         elif sum(possible[i][j]) == 0:
                              return None
               if change:
                    break

     # checks if the board is solved
     solved : bool = True
     i : int
     for i in range(9):
          j : int
          for j in range(9):
               if newField[i][j] is None:
                    solved = False
     if solved:
          return newField

     # finds cells with smallest number of possible values to recurse on
     possible = pencil9x9(field)
     minPossible : int = 16
     minI : int = None
     minJ : int = None

     i : int
     for i in range(9):
          j : int
          for j in range(9):
               if newField[i][j] is None:
                    if sum(possible[i][j]) < minPossible:
                         minPossible = sum(possible[i][j])
                         minI = i
                         minJ = j

     # recurses on the cell with the smallest number of possible values
     tempField : List[List[int or None]] = deepcopy(newField)

     i : int
     for i in range(9):
          if possible[minI][minJ][i]:
               tempField[minI][minJ] = i + 1
               
               attemptField = solveSudoku(tempField)
               if attemptField != None:
                    return attemptField
     
     return None #TODO this is a code hole

def verify9x9(field : List[List[int or None]]) -> bool: #TODO test
     '''Takes in a sudoku board, and returns True iff the board is valid, False otherwise.
     '''
     assert type(field) is list
     assert len(field) == 9
     assert all(type(i) is list for i in field)
     assert all(len(i) == 9 for i in field)
     assert all(all(type(j) is int or j is None for j in i) for i in field)

     possible : List[List[List[bool]]] = [[[False for _ in range(16)] for _ in range(9)] for _ in range(9)]

     valid : bool = True
     i : int
     for i in range(9):
          j : int
          for j in range(9):
               if field[i][j] is None: # checks that an empty cell has the possibility of being filled in
                    possible = pencil9x9_singleCell(field, i, j)
                    if sum(possible) == 0:
                         valid = False
               else: # checks that a filled cell has a penciled value such that the value of that cell is possible
                    tempField : List[List[int or None]] = deepcopy(field)
                    tempField[i][j] = None

                    possible = pencil9x9_singleCell(tempField, i, j)
                    if possible[field[i][j] - 1] == False:
                         valid = False
     return valid

if __name__ == "__main__":

     #TODO setup debug logging

     field : List[List[int]] = [[None for _ in range(9)] for _ in range(9)]

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
     
     field = stringToField(testField)

     print(field9x9_toString(field))

     possible : List[List[List[bool]]] = [[[False for _ in range(16)] for _ in range(9)] for _ in range(9)]

     possible = pencil9x9(field)

     print(field9x9_toString(field, possible))

     print(field9x9_toString(solveSudoku(field)))

     print(verify9x9(solveSudoku(field)))

