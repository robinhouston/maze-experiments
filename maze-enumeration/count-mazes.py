import itertools

from numpy import array
from numpy.linalg import eigvalsh

EPSILON = 1.0e-10

class LoopyWeavesException(Exception):
  pass

class Node(object):
  _next_id = 0
  
  def __init__(self):
    self._parent = None
    self._id = self._next_id
    self.__class__._next_id += 1
  
  def _root(self):
    if self._parent is None:
      return self
    else:
      self._parent = self._parent._root()
      return self._parent
  
  def identify_with(self, other):
    self._root()._parent = other
  
  def __eq__(self, other):
    return self._root()._id == other._root()._id
  def __ne__(self, other):
    return self._root()._id != other._root()._id
  def __hash__(self):
    return hash(self._root()._id)

class WeaveMaze(object):
  def __init__(self, num_rows, num_cols, crossings=set()):
    #print num_rows, num_cols, crossings
    self.num_rows = num_rows
    self.num_cols = num_cols
    self.crossings = set(crossings)
    
    self.node_by_cell = dict(( ((x,y), Node()) for x in range(num_cols) for y in range(num_rows) ))
    for x,y in sorted(self.crossings):
      if self._nnc(x,y,-1,0) == self._nnc(x,y,+1,0) \
      or self._nnc(x,y,0,-1) == self._nnc(x,y,0,+1):
        raise LoopyWeavesException()
      
      if (x+1,y) not in self.crossings:
        self._nnc(x,y,-1,0).identify_with(self.node_by_cell[(x+1,y)])
      if (x,y+1) not in self.crossings:
        self._nnc(x,y,0,-1).identify_with(self.node_by_cell[(x,y+1)])
    
    self.edges = set((
      ((x, y), (x+1, y)) for x in range(num_cols-1) for y in range(num_rows)
      if (x, y) not in self.crossings and (x+1, y) not in self.crossings
    )) | set((
      ((x, y), (x, y+1)) for x in range(num_cols) for y in range(num_rows-1)
      if (x, y) not in self.crossings and (x, y+1) not in self.crossings
    ))
  
  def _nnc(self, x, y, dx, dy):
    while True:
      x, y = x + dx, y + dy
      if (x,y) not in self.crossings:
        return self.node_by_cell[(x,y)]
  
  def matrix(self):
    dim = self.num_rows * self.num_cols
    matrix = array([ [ 0 for i in range(dim) ] for i in range(dim) ])
    
    index_by_node = dict(( (n, i) for i, n in enumerate(set(self.node_by_cell.values())) ))
    for sc, tc in self.edges:
      sn, tn = self.node_by_cell[sc], self.node_by_cell[tc]
      si, ti = index_by_node[sn], index_by_node[tn]
      matrix[si][si] += 1
      matrix[ti][ti] += 1
      matrix[si][ti] -= 1
      matrix[ti][si] -= 1
    
    return matrix
  
  def count(self):
    evs = eigvalsh( self.matrix() )
    non_zero_evs = [ v for v in evs if v > EPSILON ]
    return int(round(
      reduce(lambda x,y: x*y, non_zero_evs, 1) / (1 + len(non_zero_evs))
    ))

def all_subsets(gen):
  items = list(gen)
  for n in range(0, len(items) + 1):
    for combo in itertools.combinations(items, n):
      yield combo

def count_weave_mazes(n):
  total = 0
  for crossings in all_subsets(itertools.product(range(1, n-1), range(1, n-1))):
    try:
      c = WeaveMaze(n, n, crossings).count() * (2 ** len(crossings))
      print "%s: %d" % (crossings, c)
      total += c
    except LoopyWeavesException:
      print "%s: LOOPS" % (crossings,)
  return total
