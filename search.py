# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
Brandon Sim
Louis Li
CS182 Problem Set 1
9/15/13

We also collaborated with Saagar Deshpande.
"""

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
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
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def parameterizedSearch(problem, FrontierDataStructure, priorityFunction=None, heuristic=None):
  """
  Parameterized, generalized search problem

  Args:
      problem: The SearchProblem object
      frontierDataStructure: the data structure to use, i.e. queue, stack, priority queue
      heuristic: a heuristic function
      
  Returns:
      The goal state and its path
  """
  # TODO make sure the changes we made were correct...
  # x[0] is the current state
  if heuristic:
    priorityFunction = lambda x: heuristic(x[0], problem)

  if priorityFunction:
    frontier = FrontierDataStructure(priorityFunction)
  else:
    frontier = FrontierDataStructure()

  visited = []
  node = problem.getStartState()
  frontier.push((node, []))
  visited.append(node)

  while not frontier.isEmpty():
    node, actionHistory = frontier.pop()

    if problem.isGoalState(node):
      return (actionHistory + [node["board"]], node)

    # All we need is the single best successor
    successors = problem.getSuccessors(node)
    best_successor = max(successors, key=lambda x: heuristic(x, problem))
    action = best_successor["board"]

    visited.append(best_successor)
    frontier.push((best_successor, actionHistory + [action] if action else []))

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  return parameterizedSearch(problem, util.Stack)

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  return parameterizedSearch(problem, util.Queue)
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  # The item is a four-tuple described in the parameterizedSearch function,
  # where x[2] is the cost required to get to the node
  return parameterizedSearch(problem, util.PriorityQueueWithFunction, lambda x: x[2])

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  return parameterizedSearch(problem, util.PriorityQueueWithFunction, None, heuristic)

    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
