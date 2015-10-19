# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "16:23, Oct. 16th, 2015"
""" This is the library file of the project of Comparison of Search Algorithms
The function solve is a solver using A* Search.
The class Node is an interface of node using in solve."""

def solve(heuristic_func, initial_node, method = 'A*', goal_node = None, revsPath_func = None):
  """ Run A* Search if the variable method is 'A*'; or Greedy Best-First Search if method is 'GBFS'.
  Using Bidirectional Search if goal_node is given.
  The variable initial_node and goal_node must be a realization of the interface AstarNode.
  The variable heuristic_func is a heuristic function whose input is a realization of AstarNode and the goal_state
  The variable revsPath_func is a function used in bi-directional search to revise the path; its input is node.getPath()
  Return [path, g] where g means the number of nodes generated"""

  if heuristic_func(initial_node) == 0:
    return [initial_node.getPath(), 0]
  
  method = method.lower()[0]
  if method not in ("a", "g", ""):
    raise TypeError("An unsupported search algorithm is given.")

  if goal_node == None:
    bi = False
  else:
    bi = True

  # frontier = [(value of the evaluation function of node n1, node n1), ... ]"""
  frontier = [(heuristic_func(initial_node), initial_node)]
  # explored = [[path],[state]]
  explored = [[],[]]
  
  if bi == True:
    frontier2 = [(heuristic_func(goal_node), goal_node)]
    explored2 = [[], []]
    
  # Function to check if a node's state in the frontier list
  def inFrontier(frontier, node):
    for n in range(len(frontier)):
      if node.getState() == frontier[n][1].getState():
        if node.getCost() < frontier[n][1].getCost():
          # Delete the node in frontier if the new node has a cheaper cost
          del frontier[n]
          return False
        return n
    return False

  # number of nodes generated
  g = 0
  while(frontier):

    # Order the nodes in the frontier list according to their evalution function's value from low to high
    frontier.sort(key = lambda x: x[0], reverse = False)
    
    # Select the node whose evaluation function has the lowest value
    current_node = frontier.pop(0)[1]
    
    # Put current_node into the explored list, because it had been explored just now.
    explored[0].append(current_node.getPath())
    explored[1].append(current_node.getState())
    
    # if current_node's state is not the goal state,
    # we need to generate the child nodes, i.e. move the blank square to any possible direction,
    # and then put these new nodes into the frontier list if they have not been explored
    for ch in current_node.getChildNodes():
      h_value = heuristic_func(ch)
      if h_value == 0:
        return [ch.getPath(), g]
      if inFrontier(frontier, ch) == False and ch.getState() not in explored[1]:
        if bi == True:
          # In Bidirecitonal Search, we need to check the intersection.
          check_r = inFrontier(frontier2, ch)
          if check_r == False:
            if ch.state in explored2[1]:
              return [ch.getPath() + revsPath_func(explored2[0][explored2[1].index(ch.getState())]), g]
          else:
            return [ch.getPath() + revsPath_func(frontier2[check_r][1].getPath()), g]
          
        if method == "a":
          # A* Search
          f = ch.getCost() + h_value
        else:
          # Greedy Best-First Search
          f = h_value
        g = g + 1
        frontier.append((f, ch))
    
    # an instance of Bi-directional Search
    # the instance from the goal_node to the initial_node 
    if bi == True:
      frontier2.sort(key = lambda x: x[0], reverse = False)
      current_node2 = frontier2.pop(0)[1]
      explored2[0].append(current_node2.getPath())
      explored2[1].append(current_node2.getState())
      for ch in current_node2.getChildNodes():
        h_value = heuristic_func(ch)
        if h_value == 0:
          return [revsPath_func(ch.getPath()), g]
        if inFrontier(frontier2, ch) == False and ch.getState() not in explored2[1]:
          check_r = inFrontier(frontier, ch)
          if check_r == False:
            if ch.getState() in explored[1]:
              return [explored[0][explored[1].index(ch.getState())] + revsPath_func(ch.getPath()), g]
          else:
            return [frontier[check_r][1].getPath() + revsPath_func(ch.getPath()), g]
          if method == "a":
            f = ch.getCost() + h_value
          else:
            f = h_value
          g = g + 1
          frontier2.append((f, ch))

  # No Solution Found
  return None
      

class Node(object):
  """ The interface of Node"""

  def getState(self):
    """ Return a node's state """
    pass
  
  def getPath(self):
    """ Return the path from the initial node to the current node"""
    pass
  
  def getCost(self):
    """ Return the cost from the initial_state to current state"""
    pass

  def getGoalState(self):
    """ Return the goal state"""
    pass
  
  def getChildNodes(self):
    """ Return all the legal child nodes of the current node"""
    pass

if __name__ == "__main__":
  print(__file__)
  print('Author: %s'%__author__)
  print('Copyright: %s'%__copyright__)
  print('License: %s'%__license__)
  print("This is the library file of the project of Comparison of Search Algorithms. It has a solver function and a Node class as the interface of node used in the solver function.")