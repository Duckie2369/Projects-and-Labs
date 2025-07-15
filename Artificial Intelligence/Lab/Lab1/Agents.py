import random

from game import Agent
from game import Directions

class DumbAgent(Agent):
    "An agent that goes East until it can't."
    def getAction(self, state):
         "The agent receives a GameState (defined in pacman.py)."
         print("Location: ", state.getPacmanPosition())
         print("Actions available: ", state.getLegalPacmanActions())
         if Directions.EAST in state.getLegalPacmanActions():
             print("Going East.")
             return Directions.EAST
         else:
             print("Stopping.")
             return Directions.STOP

class RandomAgent(Agent):
    def getAction(self, state):
        "Array for random actions"
        drts = [Directions.EAST, Directions.WEST, Directions.SOUTH, Directions.NORTH, Directions.STOP]
        i = random.randrange(0, 5)
        "The agent receives a GameState (defined in pacman.py)."
        if drts[i] in state.getLegalPacmanActions():
            return drts[i]
        else:
            return Directions.STOP

class BetterRandomAgent(Agent):
    def getAction(self, state):
        "Array for random actions"
        drts = [Directions.EAST, Directions.WEST, Directions.SOUTH, Directions.NORTH]
        i = random.randrange(0, 4)
        "The agent receives a GameState (defined in pacman.py)."
        if drts[i] in state.getLegalPacmanActions():
            return drts[i]
        else:
            return Directions.STOP

class ReflexAgent(Agent):
    def getAction(self, state):

        "Array for random actions"
        drts = [Directions.EAST, Directions.WEST, Directions.SOUTH, Directions.NORTH]
        i = random.randint(0,3)
        "The agent receives a GameState (defined in pacman.py)."
        xP, yP = state.getPacmanPosition()
        currentFood = state.getFood()

        if (currentFood[xP-1][yP] is True):
            return Directions.WEST
        elif (currentFood[xP+1][yP] is True):
            return Directions.EAST
        elif (currentFood[xP][yP-1] is True):
            return Directions.SOUTH
        elif (currentFood[xP][yP+1] is True):
            return Directions.NORTH
        elif drts[i] in state.getLegalPacmanActions():
            return drts[i]
        else:
            return Directions.STOP


