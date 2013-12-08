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

import util
import copy
import tetris

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

    # this is bad
    #if problem.isGoalState(node):
    #  print "HERE"
    #  return (actionHistory + [node["board"]], node)

    
    successors = problem.getSuccessors(node)

    # if no successors, game over
    if len(successors) == 0:
      print "Game Over"
      return (actionHistory + [node["board"]], node)


    # generates real successors, with lines cleared
    real_successors = []
    for s in successors:
      grid_copy = copy.deepcopy(s["board"])
      clear_lines(grid_copy)
      real_successors.append({
        "board": grid_copy,
        "pieces": s["pieces"]
      })


    # All we need is the single best successor (out of the real successors)
    best_successor = max(real_successors, key=lambda x: heuristic(x, problem))
    best_index = real_successors.index(best_successor)
    old_action = successors[best_index]["board"]
    action = best_successor["board"]

    # have to check string equality for some reason due to weird ascii things
    # list equality always returns false
    if str(old_action) == str(action):
      # no lines were cleared
      newActionList = [action]
    # else push the uncleared version, then cleared one for display purposes
    else:
      newActionList = [old_action] + [action]

    new_history = actionHistory + newActionList
    visited.append(best_successor)
    frontier.push((best_successor, new_history if action else []))

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

def clear_lines(grid):
  """
  Clear lines from a grid. Mutates grid.
  
  Taken from tetris.py, Tetris.clear_lines()
  
  Returns:
      True if more than 0 lines were cleared. False otherwise
  """
  count=0
  for i in range(20):
      full=True
      for j in range(10):
          if(grid[i][j] is None): 
              full=False
              break
      if(full):
          count+=1
          for j in range(10):
              grid[i][j]=None
  i=19
  j=18
  while(i>0 and j>=0):
      null=True
      for k in range(10):
          if(grid[i][k] is not None):
              null=False
              break
      if(null):
          j=min(i-1,j)
          while(j>=0 and null):
              null=True
              for k in range(10):
                  if(grid[j][k] is not None):
                      null=False
                      break
              if(null): j-=1
          if(j<0): break
          for k in range(10):
              grid[i][k]=grid[j][k]
              grid[j][k]=None
              if(grid[i][k] is not None): grid[i][k].y=tetris.HALF_WIDTH+i*tetris.FULL_WIDTH
          j-=1
      i-=1
  
  if (count > 0):
      return True
  else:
      return False
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
