# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    from game import Directions

    directionDict = {'North':Directions.NORTH, 'South':Directions.SOUTH,
                     'East':Directions.EAST, 'West':Directions.WEST}
    frontier = util.Stack()
    visited = []
    node = {}
    node["parent"] = None
    node["action"] = None
    node["state"] = problem.getStartState()
    node["cost"] = 0
    visited.append(node["state"])
    frontier.push(node)

    def search(frontier, visited):
        if not frontier.isEmpty():
            current = frontier.pop()
            if problem.isGoalState(current["state"]):
                queue = util.Queue()
                while current["parent"]:
                    queue.push(current["action"])
                    current = current["parent"]
                return queue.list
            for next in problem.getSuccessors(current["state"]):
                if next[0] not in visited:
                    node = {}
                    node["parent"] = current
                    node["action"] = directionDict[next[1]]
                    node["state"] = next[0]
                    node["cost"] = current["cost"] + next[2]
                    visited.append(node["state"])
                    frontier.push(node)
            return search(frontier, visited)

    return search(frontier, visited)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from game import Directions

    directionDict = {'North':Directions.NORTH, 'South':Directions.SOUTH,
                     'East':Directions.EAST, 'West':Directions.WEST}
    frontier = util.Queue()
    visited = []
    node = {}
    node["parent"] = None
    node["action"] = None
    node["state"] = problem.getStartState()
    node["cost"] = 0
    visited.append(node["state"])
    frontier.push(node)

    def search(frontier, visited):
        if not frontier.isEmpty():
            current = frontier.pop()
            if problem.isGoalState(current["state"]):
                queue = util.Queue()
                while current["parent"]:
                    queue.push(current["action"])
                    current = current["parent"]
                return queue.list
            for next in problem.getSuccessors(current["state"]):
                if next[0] not in visited:
                    node = {}
                    node["parent"] = current
                    node["action"] = directionDict[next[1]]
                    node["state"] = next[0]
                    node["cost"] = current["cost"] + next[2]
                    visited.append(node["state"])
                    frontier.push(node)
            return search(frontier, visited)

    return search(frontier, visited)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from game import Directions

    directionDict = {'North':Directions.NORTH, 'South':Directions.SOUTH,
                     'East':Directions.EAST, 'West':Directions.WEST}
    frontier = util.PriorityQueue()
    visited = []
    node = {}
    node["parent"] = None
    node["actions"] = []
    node["state"] = problem.getStartState()
    node["cost"] = 0
    visited.append(node["state"])
    frontier.push(node, node["cost"])

    def search(frontier, visited):
        if not frontier.isEmpty():
            current = frontier.pop()
            if problem.isGoalState(current["state"]):
                return current["actions"]
            for next in problem.getSuccessors(current["state"]):
                if next[0] not in visited:
                    node = {}
                    node["parent"] = current
                    node["actions"] = current["actions"] + [directionDict[next[1]]]
                    node["state"] = next[0]
                    node["cost"] = problem.getCostOfActions(node["actions"])
                    visited.append(node["state"])
                    frontier.push(node, node["cost"])
            return search(frontier, visited)

    return search(frontier, visited)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from game import Directions

    directionDict = {'North':Directions.NORTH, 'South':Directions.SOUTH,
                     'East':Directions.EAST, 'West':Directions.WEST}
    frontier = util.PriorityQueue()
    visited = []
    node = {}
    node["parent"] = None
    node["actions"] = []
    node["state"] = problem.getStartState()
    node["cost"] = 0
    visited.append(node["state"])
    frontier.push(node, node["cost"])

    def search(frontier, visited):
        if not frontier.isEmpty():
            current = frontier.pop()
            if problem.isGoalState(current["state"]):
                return current["actions"]
            for next in problem.getSuccessors(current["state"]):
                if next[0] not in visited:
                    node = {}
                    node["parent"] = current
                    node["actions"] = current["actions"] + [directionDict[next[1]]]
                    node["state"] = next[0]
                    node["cost"] = (problem.getCostOfActions(node["actions"]) +
                                    heuristic(node["state"], problem))
                    visited.append(node["state"])
                    frontier.push(node, node["cost"])
            return search(frontier, visited)

    return search(frontier, visited)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
