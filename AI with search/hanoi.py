![[ ! -d "aipython" ]] && wget https://artint.info/AIPython/aipython.zip && unzip -q aipython.zip
# access the aipython resources
import sys
if 'aipython' not in sys.path:
    sys.path.append('aipython')

from searchProblem import Arc, Search_problem
from searchGeneric import FrontierPQ, AStarSearcher
from searchGeneric import Searcher as DepthFirstSearcher

class BreadthFirstSearcher(DepthFirstSearcher):

    def add_to_frontier(self,path):
        # we change the original implementation so that the frontier is now FIFO, i.e. new nodes
        # are added at the front of the list, the algorithm "pops" them off from the end
        self.frontier.insert(0,path)

class GreedyBestFirstSearcher(DepthFirstSearcher):

    def __init__(self, problem):
        super().__init__(problem)

    def initialize_frontier(self):
        self.frontier = FrontierPQ()

    def empty_frontier(self):
        return self.frontier.empty()

    def add_to_frontier(self,path):
        """add path to the frontier with the appropriate heuristic"""
        value = self.problem.heuristic(path.end())
        self.frontier.add(path, value)

class Hanoi(Search_problem):
  """Class representing instances of the maze problem"""

  def __init__(self, pegs, rings):
    """Create a square instance with the given size and set of blocked tiles"""
    self.pegs = pegs
    self.rings = rings
    self.initial_state = [list(range(1, rings + 1))] + [[] for _ in range(pegs - 1)]

  def start_node(self):
    """Return the starting position of the agent"""
    return self.initial_state

  def is_goal(self,node):
    """True is the given state represents the target cell"""
    return node == [[] for _ in range(self.pegs - 1)] + [list(range(1, self.rings + 1))]

  def neighbors(self,node):
    """Return a list of the arcs for the possible neighbouring states"""  
    actions = []
    for src in range(self.pegs):  # Iterate through each peg
      if not node[src]:  # If the peg is empty, skip it
        continue    
      for dest in range(self.pegs):  # Iterate through destination pegs
        if src == dest:  # Can't move a ring onto the same peg
          continue
        if not node[dest] or node[src][0] < node[dest][0]:  # Move if empty OR smaller ring on top
          new_state = [peg[:] for peg in node]  # Make a copy of the current state
          ring = new_state[src].pop(0)  # Remove the top ring from source
          new_state[dest].insert(0, ring)  # Move it to the destination

          actions.append(Arc(node, new_state, action=f"Move r{ring} from {src} to {dest}"))

    return actions

        # if r > 0 and (r-1,c) not in self.blocked:
        #     actions.append(Arc(node,(r-1,c),action="up"))
        # if r < self.size-1 and (r+1,c) not in self.blocked:
        #     actions.append(Arc(node,(r+1,c),action="down"))
        # if c > 0 and (r,c-1) not in self.blocked:
        #     actions.append(Arc(node,(r,c-1),action="left"))
        # if c < self.size-1 and (r,c+1) not in self.blocked:
        #     actions.append(Arc(node,(r,c+1),action="right"))
        # random.shuffle(actions)
        # return actions

    # def heuristic(self,node):
    #     """Return the Manhattan distance to the goal"""
    #     r,c = node
    #     last = self.size-1
    #     return abs(r-last) + abs(c-last)

puz = Hanoi(3,3)
s = BreadthFirstSearcher(puz)
s.search()
