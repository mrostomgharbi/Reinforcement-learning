"""
This is one of the most important codes to run the game.
This is actually what the user sees when he plays.
"""
import os

class Board:
    """
    This class represents the game's board.
    """

    def __init__(self):
        self._rows = []
        for row_index in range(6):
            row = [" " for _ in range(7)]
            self._rows.append(row)

    def __str__(self):
        nl = os.linesep
        s = nl
        for row in reversed(self._rows):
            row_str = ""
            for spot in row:
                if spot == ' ':
                    row_str += "|___"
                else:
                    row_str += "|_" + spot + "_"
            row_str += "|" + nl
            s += row_str
        
        for i in range(7):
        	s = ' ___' + s

        rng = [str(i) for i in range(7)]
        nums = "   ".join(rng)
        s += nl + "  " + nums
        return s

    def place(self, move, symbol):
        """
        This function helpus us place the new symbol on the board after a given location.
        """
        assert(symbol == 'x' or symbol == 'o')
        assert(self.valid_move(move))
        r = self._find_row_from_col(move)
        self._rows[r][move] = symbol

    def four_in_a_row(self):
        """
        This function helps us to know if there is a winner.
        Whenever we have 4 marks in a row, the game is over.
        This function returns True if x or if o has four in a row.
        In addition to that, it returns the winner of the game.
        """
        rows, winner = self._check_for_four(self._rows)
        if rows:
            return True, winner
        cols, winner = self._check_for_four(self._cols())
        if cols:
            return True, winner
        diag, winner = self._check_for_four(self._diagonals())
        if diag:
            return True, winner

        return False, None

    def valid_move(self, move):
        """
        This function checks if the move is valid or not.
        """
        return not self._column_is_full(move)

    def _check_for_four(self, ls):
        """
        This function actually completes the four in a row function.
        Here we check in there are 4 succesive marks, wether its in columns, raw, or diagonal. 
        """
        for row_col_or_diag in ls:
            num_in_a_row = 0
            last_seen = None
            for spot in row_col_or_diag:
                if spot == last_seen and spot != ' ':
                    num_in_a_row += 1
                else:
                    last_seen = spot
                    num_in_a_row = 1
                if num_in_a_row >= 4:
                    return True, last_seen
        return False, ' '

    def _column_is_full(self, col_index):
        """
        When the column is full, we can not add more marks to it. 
        With this function we check if a column is full or not. 
        """
        column = [row[col_index] for row in self._rows]
        for spot in column:
            if spot == ' ':
                return False
        return True

    def _cols(self):
        for i in range(7):
            yield [row[i] for row in self._rows]

    def _diagonals(self):
        for j in range(3, 9):
            yield [self._rows[i][j - i] for i in range(len(self._rows))\
                    if (j - i) < 7 and (j - i) >= 0]

        for j in range(-2, 3):
            yield [self._rows[i][i + j] for i in range(len(self._rows))\
                    if (i + j) < 7 and (i + j) >= 0]

    def _find_row_from_col(self, col_index):
        """
        Finds the right row from the given column
        """
        column = [row[col_index] for row in self._rows]
        for i, spot in enumerate(column):
            # Looking from the bottom row up
            if spot == ' ':
                return i








