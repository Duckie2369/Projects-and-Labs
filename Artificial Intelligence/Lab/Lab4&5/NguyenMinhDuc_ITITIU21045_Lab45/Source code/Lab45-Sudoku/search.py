"""
In search.py, you will implement Backtracking and AC3 searching algorithms
for solving Sudoku problem which is called by sudoku.py
"""

from csp import *
from copy import deepcopy
import queue



def Backtracking_Search(csp):
    """
    Backtracking search initializes the initial assignment
    and calls the recursive backtrack function.
    """
    assignment = {}
    for var in squares:
        if len(csp.values[var]) == 1:
            assignment[var] = csp.values[var]
    return Recursive_Backtracking(assignment, csp)

def Recursive_Backtracking(assignment, csp):
    """
    The recursive function which assigns value using backtracking
    with improved efficiency
    """
    # Check if assignment is complete
    if isComplete(assignment):
        return assignment

    # Select unassigned variable using MRV
    var = Select_Unassigned_Variables(assignment, csp)

    # Get possible values for the variable
    domain = Order_Domain_Values(var, assignment, csp)

    # Try each value
    for value in domain:
        if isConsistent(var, value, assignment, csp):
            # Save current state
            saved_values = deepcopy(csp.values)

            # Make assignment
            assignment[var] = value
            forward_checking(csp, assignment, var, value)

            # Try inference
            inferences = {}
            result = Inference(assignment, inferences, csp, var, value)

            if result != "FAILURE":
                # Add inferences to assignment
                assignment.update(inferences)

                # Recursive call
                result = Recursive_Backtracking(assignment, csp)
                if result is not None:
                    return result

                # Remove inferences if backtracking
                for key in inferences:
                    assignment.pop(key, None)

            # Backtrack: restore previous state
            assignment.pop(var, None)
            csp.values = saved_values

    return None


def AC3(csp):
    """
    AC3 algorithm for constraint propagation.
    Returns a solution dictionary if solved, "FAILURE" if unsolvable.
    """
    # Initialize queue with all binary constraints
    queue = list(csp.constraints)

    while queue:
        (xi, xj) = queue.pop(0)

        if Revise(csp, xi, xj):
            # If domain of xi is empty, this branch has failed
            if len(csp.values[xi]) == 0:
                return "FAILURE"

            # Add all neighboring arcs to queue for further processing
            for xk in (csp.peers[xi] - {xj}):
                queue.append((xk, xi))

    # Convert to solution format (same as Backtracking_Search)
    solution = {}
    for var in squares:
        if len(csp.values[var]) == 1:
            solution[var] = csp.values[var]
        else:
            return "FAILURE"  # Puzzle not completely solved

    return solution


def Revise(csp, xi, xj):
    """
    Returns true if we revise the domain of xi with respect to xj.
    """
    revised = False
    values_to_remove = set()

    # Check each value in xi's domain
    for x in csp.values[xi]:
        # Get all values in xj's domain
        conflict = True
        for y in csp.values[xj]:
            if x != y:
                conflict = False
                break

        if conflict:
            values_to_remove.add(x)
            revised = True

    # Remove all invalid values from xi's domain
    for value in values_to_remove:
        csp.values[xi] = csp.values[xi].replace(value, '')

    return revised


def Inference(assignment, inferences, csp, var, value):
    """
    Forward checking using concept of Inferences
    """

    inferences[var] = value

    for neighbor in csp.peers[var]:
        if neighbor not in assignment and value in csp.values[neighbor]:
            if len(csp.values[neighbor]) == 1:
                return "FAILURE"

            remaining = csp.values[neighbor] = csp.values[neighbor].replace(value, "")

            if len(remaining) == 1:
                flag = Inference(assignment, inferences, csp, neighbor, remaining)
                if flag == "FAILURE":
                    return "FAILURE"

    return inferences


def Order_Domain_Values(var, assignment, csp):
    """
    Returns string of values of given variable
    """
    return csp.values[var]


def Select_Unassigned_Variables(assignment, csp):
    """
    Selects new variable to be assigned using minimum remaining value (MRV)
    """
    unassigned_variables = dict((squares, len(csp.values[squares])) for squares in csp.values if squares not in assignment.keys())
    mrv = min(unassigned_variables, key=unassigned_variables.get)
    return mrv


def isComplete(assignment):
    """
    Check if assignment is complete
    """
    return set(assignment.keys()) == set(squares)


def isConsistent(var, value, assignment, csp):
    """
    Check if assignment is consistent
    """
    for neighbor in csp.peers[var]:
        if neighbor in assignment.keys() and assignment[neighbor] == value:
            return False
    return True


def forward_checking(csp, assignment, var, value):
    csp.values[var] = value
    for neighbor in csp.peers[var]:
        csp.values[neighbor] = csp.values[neighbor].replace(value, '')


def display(values):
    """
    Display the solved sudoku on screen
    """
    for row in rows:
        if row in 'DG':
            print("-------------------------------------------")
        for col in cols:
            if col in '47':
                print(' | ', values[row + col], ' ', end=' ')
            else:
                print(values[row + col], ' ', end=' ')
        print(end='\n')


def write(values):
    """
    Write the string output of solved sudoku to file
    """
    output = ""
    for variable in squares:
        output = output + values[variable]
    return output


