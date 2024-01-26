# Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in the Python 3.9.4 programming environment

import random
import os


def Main():
    """
    Starts the game.
    No parameters or returns.
    """

    Again = "y"
    Score = 0
    while Again == "y":
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
        Score = MyPuzzle.AttemptPuzzle()
        print("Puzzle finished. Your score was: " + str(Score))
        Again = input("Do another puzzle? ").lower()


class Puzzle():
    def __init__(self, *args):
        """
        Initialises Puzzle class and defines its properties

        Parameters
        ----------
        *args: list of args to define the Puzzle properties
        """

        if len(args) == 1:
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            QPattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")
            LPattern = Pattern("L", "L***LLLL*")
            self.__AllowedPatterns.append(LPattern)
            self.__AllowedSymbols.append("L")

    def __SavePuzzle(self, Filename):
        with open(Filename, 'w') as f:
            f.write(f"{len(self.__AllowedSymbols)}\n")
            for symbol in self.__AllowedSymbols:
                f.write(f"{symbol}\n")
            f.write(f"{len(self.__AllowedPatterns)}\n")
            for pattern in self.__AllowedPatterns:
                f.write(f"{pattern.__Symbol()},{pattern.GetPatternSequence()}\n")
            f.write(f"{self.__GridSize}\n")
            for cell in self.__Grid:
                if isinstance(cell, BlockedCell):
                    f.write('@,\n')
                else:
                    f.write(f"{cell._Symbol},{cell.__SymbolsNotAllowed}\n")

            f.write(f"{self.__Score}\n")
            f.write(f"{self.__SymbolsLeft}\n")


    def __LoadPuzzle(self, Filename):
        """
        Loads a Puzzle from a given file.

        Parameters
        ----------
        Filename: txt file with the info for a Puzzle layout
        """

        try:
            with open(Filename) as f:
                NoOfSymbols = int(f.readline().rstrip())
                for Count in range(1, NoOfSymbols + 1):
                    self.__AllowedSymbols.append(f.readline().rstrip())
                NoOfPatterns = int(f.readline().rstrip())
                for Count in range(1, NoOfPatterns + 1):
                    Items = f.readline().rstrip().split(",")
                    P = Pattern(Items[0], Items[1])
                    self.__AllowedPatterns.append(P)
                self.__GridSize = int(f.readline().rstrip())
                for Count in range(1, self.__GridSize * self.__GridSize + 1):
                    Items = f.readline().rstrip().split(",")
                    if Items[0] == "@":
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else:
                        C = Cell()
                        C.ChangeSymbolInCell(Items[0])
                        for CurrentSymbol in range(1, len(Items)):
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                        self.__Grid.append(C)
                self.__Score = int(f.readline().rstrip())
                self.__SymbolsLeft = int(f.readline().rstrip())
        except:
            print("Puzzle not loaded")

    def AttemptPuzzle(self):
        """
        Allows the user to play the Puzzle and input symbols.

        Returns
        -------
        self.__Score : int, the user's total score
        """

        Finished = False
        while not Finished:
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
            Row = -1
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass
            Symbol = self.__GetSymbolFromUser()
            self.__SymbolsLeft -= 1
            CurrentCell = self.__GetCell(Row, Column)
            if CurrentCell.CheckSymbolAllowed(Symbol):
                CurrentCell.ChangeSymbolInCell(Symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore
            if self.__SymbolsLeft == 0:
                Finished = True
        print()
        self.DisplayPuzzle()
        print()
        return self.__Score

    def __GetCell(self, Row, Column):
        """
        Finds the coords of the cell requested by its row and column

        Parameters
        ----------
        Row : int, row number of target cell
        Column: int, column number of target cell

        Returns
        -------
        self.__Grid[Index] : Cell
        """

        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()

    def CheckforMatchWithPattern(self, Row, Column):
        """
        Checks if the 3 by 3 grid of the current cell has symbols that match a correct pattern

        Parameters
        ----------
        Row : int, the row number of the cell to check
        Column : int, the column number of the cell to check

        Returns
        -------
        10 if symbols match pattern
        0 if not
        """

        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                except:
                    pass
        return 0

    def __GetSymbolFromUser(self):
        """
        Asks the user for the symbol they want to enter

        Returns
        -------
        Symbol : str, the symbol given by the user
        """

        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol

    def __CreateHorizontalLine(self):
        """
        Draws a horizontal dashed line on the grid denoting different rows

        Returns
        -------
        Line : str, the line created
        """

        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    def DisplayPuzzle(self):
        """
        Displays the Puzzle by printing each row
        """

        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())


class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        """
        Initialises Pattern class and defines its properties

        Parameters
        ----------
        SymbolToUse : str, the symbol corresponding to the wanted pattern
        PatternString : str, the pattern string created from the symbol
        """

        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString

    def MatchesPattern(self, PatternString, SymbolPlaced):
        """
        Checks if the pattern matches one of the correct patterns

        Parameters
        ----------
        PatternString : str, pattern to match
        SymbolPlaced : str, symbol added to pattern

        Returns
        -------
        bool : True or False depending on if pattern matches or not
        """

        if SymbolPlaced != self.__Symbol:
            return False
        for Count in range(0, len(self.__PatternSequence)):
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    def GetPatternSequence(self):
        """
        Gets the pattern sequence to match against

        Returns
        -------
        self.__PatternSequence : str, pattern as a string
        """

        return self.__PatternSequence


class Cell():
    def __init__(self):
        """
        Initialises Cell class and defines its properties
        """

        self._Symbol = ""
        self.__SymbolsNotAllowed = []
        self.blocked = False

    def GetSymbol(self):
        """
        Gets the symbol currently in the cell

        Returns
        -------
        '-' : str, if cell is empty
        self._Symbol : str, if cell has a symbol
        """

        if self.IsEmpty():
            return "-"
        else:
            return self._Symbol

    def IsEmpty(self):
        """
        Checks if the cell has no symbol in it

        Returns
        -------
        True : bool, if the cell is empty
        False : bool, if there is a symbol in the cell
        """

        if len(self._Symbol) == 0:
            return True
        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        """
        Changes the symbol held in the cell to the chosen symbol

        Parameters
        ----------
        NewSymbol : str, the symbol being written to the cell
        """

        self._Symbol = NewSymbol
        self.blocked = True
        # blocks cell if it's been edited.

    def CheckSymbolAllowed(self, SymbolToCheck):
        """
        Checks if the symbol is allowed in that cell (sees if there are already too many in that 3 by 3 grid)

        Parameters
        ----------
        SymbolToCheck : symbol given to check if allowed

        Returns
        -------
        True : bool, if allowed
        False : bool, if not allowed
        """

        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False

        if self.blocked:
            return False
        else:
            return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        """
        Adds given symbol into list with all the symbols that are not allowed

        Parameters
        ----------
        SymbolToAdd : str, the symbol to add to not allowed list
        """

        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        """
        pass
        """

        pass


class BlockedCell(Cell):
    def __init__(self):
        """
        Initialises the Blocked Cell class and defines its properties. It inherits from the Cell class.
        """

        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        """
        Checks if the given symbol is allowed to be placed

        Parameters
        ----------
        SymbolToCheck : symbol to check

        Returns
        -------
        False
        """

        return False


if __name__ == "__main__":
    Main()
