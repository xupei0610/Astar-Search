# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "16:45, Oct. 16th, 2015"
""" This is library of the realization of sliding puzzle problem in the project of Comparison of Search Algorithms.
A one-dimensional list is used to represent a state.
e.g. In the state below
  [ N11, N12, N13,
    N21, N22, N23,
    N31, N32, N33 ]
  Nij represents the number in the square locating at the joint of row i and col j.
  And, if Nmn = 0, it represents that a blank square locates at the joint of row m and col n.  

The default goal state of a sliding puzzle problem is like:
  [1, 2, 3, 4, 5, 6, 7, 8, 0]"""

import random, copy
import Astar

def generateInitialState(size=3):
  """ Randomly Generate a *solvable* sliding puzzle's initial state according to the game size given.
  Supported size is 3 for '3x3', 4 for '4x4' and the like."""
  state = random.sample([x for x in range(size**2)], size**2)
  if isSolvable(state):
    return state
  else:
    return generateInitialState(size)

def generateInitialNode(initial_state = None, goal_state = None):
  """ Generate the initial node, whose goal state is the same to the variable goal_state, according to the initial_state given or to the initial_state generated randomly.
  The default goal state is the state where the slot in the sliding puzzle is located at the right-bottom corner.
  Return an instance of the interface Astar.Node()""" 
  if initial_state == None:
    initial_state = generateInitialState()
  state_size = len(initial_state)
  side_size = int(state_size**0.5)
  if side_size != state_size**0.5:
      raise TypeError("An illegal initial state is given.")
  if goal_state == None:
      goal_state = [ x for x in range(state_size)]
  if sorted(initial_state) == sorted(goal_state):
    return Node(initial_state = initial_state, goal_state = goal_state)
  else:
    raise TypeError("An illegal initial or goal state is given.")

def isSolvable(state):
  """ Return True if the given state is a solvable game state; Return False otherwise"""
  # see: http://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
  state_size = len(state)
  side_size = int(state_size**0.5)
  if side_size == state_size**0.5:
    if sorted(state) == [ x for x in range(state_size)]:
      game_size = (side_size, state_size)
    else:
      raise TypeError("An illegal initial state is given.")
  else:
    raise TypeError("An illegal initial state is given.")
    
  inversions = 0
  for i in range(game_size[1]-1):
    if state[i] != 0:
      count = 1
      for j in range(i):
        if state[j] != 0 and state[j] < state[i]:
          count = count + 1
      inversions = inversions + state[i] - count
  
  if game_size[0] % 2 == 1:
    if inversions % 2 == 0:
      return True
  else:
    blank_position = state.index(0)
    if (game_size[0] - divmod(blank_position, game_size[0])[0]) % 2 == 0:
      if inversions % 2 == 1:
        return True
    else:
      if inversions % 2 == 0:
        return True
  return False


class Node(Astar.Node):
  """An realization of the interface Astar.Node()"""

  def __init__(self, parent_node = None, action = None, initial_state = None, goal_state = None):
    """ Generate a child node according to parent_node and action; Or generate a node whose state is initial_state and whose goal is to reach goal_state"""
    if parent_node:
      # Generate a child node of the parent node according to the action given
      self.game_size = parent_node.game_size
      self.goal_state = parent_node.goal_state
      self.state = self.move(parent_node.state, action)
      self.path = parent_node.path + action
      self.cost = parent_node.cost + 1

    elif initial_state and goal_state:
      # Generate the initial node
      state_size = len(initial_state)
      side_size = int(state_size**0.5)
      self.game_size = (side_size, state_size)
      self.path = ''
      self.state = initial_state
      self.cost = 0
      self.goal_state = goal_state

    else:
      raise TypeError("A parent node and action or an initial state and goal state should be given for generating a node")
  
  def getPath(self):
    """ Realization of Astar.Node.getPath()"""
    return self.path
    
  def getCost(self):
    """ Realization of Astar.Node.getCost()"""
    return self.cost
    
  def getState(self):
    """ Realization of Astar.Node.getState()"""
    return self.state
  
  def getGoalState(self):
    """ Realization of Astar.Node.getGoalState()"""
    return self.goal_state
  
  def getChildNodes(self):
    """ Realization of Astar.Node.getChildNodes()"""
    return self.childNodes()
  
  def childNodes(self):
    """ Return all legal child nodes of the current node."""
    child_nodes = []
    actions = ["u", "d", "l", "r"]
    if self.path:
      last_act = self.path[-1]
      if last_act == 'u':
        del actions[1]
      elif last_act =='d':
        del actions[0]
      elif last_act == 'l':
        del actions[3]
      elif last_act == 'r':
        del actions[2]
    for act in actions:
      if self.canMove(act):
        child_nodes.append(Node(parent_node = self, action = act)) 
    return child_nodes

  def canMove(self, direction):
    """ Return True if the blank square or slot in the current node's state space can move along the given direction.
    Return False otherwise"""
    blank_position = self.state.index(0)
    if direction == 'u':
      if blank_position - self.game_size[0] > -1:
        return True
    elif direction == 'd':
      if blank_position + self.game_size[0] < self.game_size[1]:
        return True
    elif direction == 'l':
      if divmod(blank_position, self.game_size[0])[1] != 0:
        return True
    elif direction == 'r':
      if divmod(blank_position, self.game_size[0])[1] != (self.game_size[0] - 1):
        return True
    return False
  
  def move(self, state, direction):
    """ Return the new state after the blank square in the given state is moved along given direction.
    Please use self.canMove() to check the legality of the move before use this function. """
    blank_position = state.index(0)
    if direction == 'u':
      destination = blank_position - self.game_size[0]
    elif direction == 'd':
      destination = blank_position + self.game_size[0]
    elif direction == 'l':
      destination = blank_position - 1
    elif direction == 'r':
      destination = blank_position + 1
    new_state = copy.deepcopy(state)
    new_state[blank_position], new_state[destination] = state[destination], state[blank_position]
    return new_state

class Heuristics():
  """ 3 kinds of heuristic algorithm functions used in A* Search is defined in this class, plus a function revsPath() for Bi-directional Search."""
  
  def manhattan(node):
    """ Heuristic Algorithm using Manhattan Distance"""
    val = 0
    for i in range(node.game_size[1]):
      if node.state[i] != 0 and node.state[i] != node.goal_state[i]:
        g_x, g_y = divmod(node.goal_state.index(node.state[i]), node.game_size[0])
        n_x, n_y = divmod(i, node.game_size[0])
        val = val + abs(g_x - n_x) + abs(n_y - g_y)
    return val
  
  def straightLine(node):
    """ Heuristic Algorithm using Straight-Line Distance"""
    val = 0
    for i in range(node.game_size[1]):
      if node.state[i] != 0 and node.state[i] != node.goal_state[i]:
        g_x, g_y = divmod(node.goal_state.index(node.state[i]), node.game_size[0])
        n_x, n_y = divmod(i, node.game_size[0])
        val = val + ((g_x - n_x)**2 + (n_y - g_y)**2)**0.5  
    return val
  
  def squaredEuclid(node):
    """ Heuristic Algorithm using Squared Euclidean Distance"""
    val = 0
    for i in range(node.game_size[1]):
      if node.state[i] != 0 and node.state[i] != node.goal_state[i]:
        g_x, g_y = divmod(node.goal_state.index(node.state[i]), node.game_size[0])
        n_x, n_y = divmod(i, node.game_size[0])
        val = val + (g_x - n_x)**2 + (n_y - g_y)**2
    return val
  
  def revsPath(path):
    """ Revise path for the instance from the goal state to the initial state in the Bi-directional Search"""
    rps = ''
    for p in path:
      if p == 'u':
        rp = 'd'
      elif p =='d':
        rp = 'u'
      elif p == 'l':
        rp = 'r'
      elif p == 'r':
        rp = 'l'
      rps = rp + rps
    return rps
    
if __name__ == "__main__":
  print(__file__)
  print('Author: %s'%__author__)
  print('Copyright: %s'%__copyright__)
  print('License: %s'%__license__)
  print("This is the library file of Sliding Puzzle. It has a function to generate a puzzle's initial state, a function to generate a initial node using the Node class defined in this file which is a realization of the interface Astar.Node(), and a static class who has the realization of 3 heuristic algorithms (Manhattan Distance, Straight Line Distance and Squared Euclidean Distance) and a function who can evise path for the instance from the goal state to the initial state in the Bi-directional Search")