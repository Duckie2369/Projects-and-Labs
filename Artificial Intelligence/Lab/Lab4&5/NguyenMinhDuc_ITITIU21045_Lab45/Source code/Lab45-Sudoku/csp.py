# CLASS DESCRIPTION FOR CONSTRAINT SATISFACTION PROBLEM (CSP)

from util import *


class csp:

    # INITIALIZING THE CSP
    def __init__(self, domain=digits, grid=""):
        """
        Initialize the Sudoku puzzle as a CSP with improved constraint handling
        """
        # Initialize basic attributes
        self.domain = domain

        # Create variables (81 cells from A1 to I9)
        self.variables = squares

        # Create unitlist more efficiently
        row_units = [[r + c for c in cols] for r in rows]
        col_units = [[r + c for r in rows] for c in cols]
        box_units = [[r + c for r in box_rows for c in box_cols]
                     for box_rows in ('ABC', 'DEF', 'GHI')
                     for box_cols in ('123', '456', '789')]
        self.unitlist = row_units + col_units + box_units

        # Create units and peers more efficiently
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in squares)

        self.peers = dict((s, set(sum(self.units[s],[]))-set([s])) for s in squares)

        # Initialize values with initial constraint propagation
        self.values = self.getDict(grid)
        self.constraints = {(variable, peer) for variable in self.variables for peer in self.peers[variable]}
        # Do initial constraint propagation
        if grid:
            for var in self.variables:
                if len(self.values[var]) == 1:
                    for peer in self.peers[var]:
                        self.values[peer] = self.values[peer].replace(self.values[var], '')

    def getDict(self, grid=""):
        """
        Getting the string as input and returning the corresponding dictionary
        """
        i = 0
        values = dict()
        for cell in self.variables:
            if grid[i] != '0':
                values[cell] = grid[i]
            else:
                values[cell] = digits
            i = i + 1
        return values