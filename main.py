from copy import deepcopy


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def __str__(self):
        return 'Row: ' + str(self.row) + '|Column: ' + str(self.col) + '|Values: ' + str(self.values)


class SubBoard:
    def __init__(self):
        self.emptyCells = []
        self.values = []
        self.tallies = {}
        self.solved = False


class Solution:
    def solveSudoku(self, board) -> None:
        """
        Do not return anything, modify board in-place instead.
        """

        def solver(subBoards, modified):
            while modified:
                modified = False
                # Removing possible values for each cell by checking the row and column
                for subBoardRow in range(3):
                    for subBoardCol in range(3):
                        currentSubBoard = subBoards[subBoardRow][subBoardCol]
                        emptyCells = currentSubBoard.emptyCells
                        for current in emptyCells:
                            for col in range(9):
                                cellValue = board[current.row][col]
                                if cellValue.isnumeric():
                                    if cellValue in current.values:
                                        current.values.remove(cellValue)
                                        modified = True
                            for row in range(9):
                                cellValue = board[row][current.col]
                                if cellValue.isnumeric():
                                    if cellValue in current.values:
                                        current.values.remove(cellValue)
                                        modified = True

                            for cellValue in currentSubBoard.values:
                                if cellValue in current.values:
                                    current.values.remove(cellValue)
                                    modified = True

                            if len(current.values) == 1:
                                board[current.row][current.col] = current.values[0]
                                emptyCells.remove(current)
                                currentSubBoard.values.append(current.values[0])
                                modified = True
                            else:
                                for value in current.values:
                                    if value in currentSubBoard.tallies:
                                        if current not in currentSubBoard.tallies[value]:
                                            currentSubBoard.tallies[value].append(current)
                                            modified = True
                                    else:
                                        currentSubBoard.tallies[value] = [current]
                                        modified = True
                        if len(emptyCells) == 0:
                            currentSubBoard.solved = True

                # Advanced tactics
                for subBoardRow in range(3):
                    for subBoardCol in range(3):
                        currentSubBoard = subBoards[subBoardRow][subBoardCol]
                        currentTallies = currentSubBoard.tallies
                        for value in list(currentTallies):
                            cells = currentTallies[value]
                            if 1 < len(cells) <= 3:
                                rowTrue = True
                                colTrue = True
                                for i in range(1, len(cells)):
                                    if cells[i].row != cells[i - 1].row:
                                        rowTrue = False
                                    if cells[i].col != cells[i - 1].col:
                                        colTrue = False
                                if rowTrue:
                                    row = cells[0].row
                                    for miniSubBoardCol in range(3):
                                        if subBoardCol == miniSubBoardCol:
                                            continue
                                        else:
                                            miniSubBoard = subBoards[subBoardRow][miniSubBoardCol]
                                            for cell in miniSubBoard.emptyCells:
                                                if cell.row == row and value in cell.values:
                                                    cell.values.remove(value)
                                                    modified = True
                                                    if value in list(miniSubBoard.tallies):
                                                        if cell in miniSubBoard.tallies[value]:
                                                            miniSubBoard.tallies[value].remove(cell)
                                if colTrue:
                                    col = cells[0].col
                                    for miniSubBoardRow in range(3):
                                        if subBoardRow == miniSubBoardRow:
                                            continue
                                        else:
                                            miniSubBoard = subBoards[miniSubBoardRow][subBoardCol]
                                            for cell in miniSubBoard.emptyCells:
                                                if cell.col == col and value in cell.values:
                                                    cell.values.remove(value)
                                                    modified = True
                                                    if value in list(miniSubBoard.tallies):
                                                        if cell in miniSubBoard.tallies[value]:
                                                            miniSubBoard.tallies[value].remove(cell)

        # Creating list of sub-boards
        # Inside sub-boards are list of empty cells and values in that sub-board
        subBoardsORG = []
        for row in range(0, 9, 3):
            subBoardRow = []
            for col in range(0, 9, 3):
                subBoard = SubBoard()
                for subRow in range(row, row + 3):
                    for subCol in range(col, col + 3):
                        value = board[subRow][subCol]
                        if value.isnumeric():
                            subBoard.values.append(value)
                        else:
                            subBoard.emptyCells.append(Cell(subRow, subCol))
                subBoardRow.append(subBoard)
            subBoardsORG.append(subBoardRow)

        changed = True
        solver(subBoardsORG, changed)
        solved = True
        for subBoardRow in range(3):
            for subBoardCol in range(3):
                currentSubBoard = subBoardsORG[subBoardRow][subBoardCol]
                if not currentSubBoard.solved:
                    solved = False
                    break
        if not solved:
            tempSubBoards = deepcopy(subBoardsORG)


sudoku_board = [["5", "3", ".", ".", "7", ".", ".", ".", "."], ["6", ".", ".", "1", "9", "5", ".", ".", "."],
                [".", "9", "8", ".", ".", ".", ".", "6", "."], ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
                ["4", ".", ".", "8", ".", "3", ".", ".", "1"], ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
                [".", "6", ".", ".", ".", ".", "2", "8", "."], [".", ".", ".", "4", "1", "9", ".", ".", "5"],
                [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

hard_board = [[".", ".", "9", "7", "4", "8", ".", ".", "."],
              ["7", ".", ".", ".", ".", ".", ".", ".", "."],
              [".", "2", ".", "1", ".", "9", ".", ".", "."],
              [".", ".", "7", ".", ".", ".", "2", "4", "."],
              [".", "6", "4", ".", "1", ".", "5", "9", "."],
              [".", "9", "8", ".", ".", ".", "3", ".", "."],
              [".", ".", ".", "8", ".", "3", ".", "2", "."],
              [".", ".", ".", ".", ".", ".", ".", ".", "6"],
              [".", ".", ".", "2", "7", "5", "9", ".", "."]]
solution = Solution()
solution.solveSudoku(hard_board)
for i in hard_board:
    print(i)
    print()
