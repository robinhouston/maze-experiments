from numpy import array
from numpy.linalg import det

class MazeEnumerator(object):
  def __init__(self, maze):
    self.maze = maze
    self._init_laplacian()
    self.n = int(round(det(self.laplacian)))
  
  def _init_laplacian(self):
    from mazer.maze import (DELTA, OPPOSITE)
    
    cc_by_c = self.maze.connected_component_by_cell()
    cc_set = set( cc_by_c.itervalues() )
    
    cc0 = cc_by_c[(0,0)]
    cc_set.remove(cc0)
    cc_list = list(cc_set)
    
    index_by_cc = dict((
      (cc, i) for i,cc in enumerate(cc_list)
    ))
    index_by_cc[cc0] = None
    
    n = len(cc_list)
    laplacian = array([ [0] * n for j in range(n) ])
    exits_by_cc = {}
    
    for x,y,d in self.maze.walls():
      dx, dy = DELTA[d]
      cc_s, cc_t = cc_by_c[(x, y)], cc_by_c[(x + dx, y + dy)]
      if cc_s == cc_t:
        continue
      i_s, i_t = index_by_cc[cc_s], index_by_cc[cc_t]
      
      exits_by_cc.setdefault(cc_s, []).append((x+dx, y+dy, OPPOSITE[d]))
      exits_by_cc.setdefault(cc_t, []).append((x, y, d))
      
      if i_s is not None:
        laplacian[i_s, i_s] += 1
      if i_t is not None:
        laplacian[i_t, i_t] += 1
      
      if i_s is not None and i_t is not None:
        laplacian[i_s, i_t] -= 1
        laplacian[i_t, i_s] -= 1
    
    self.laplacian = laplacian
    self.cc0 = cc0
    self.exits_by_cc = exits_by_cc
    self.index_by_cc = index_by_cc
  
  def nth_completion(self, i):
    rmin, rmax = 0, self.n
    exits_from_cc0 = self.exits_by_cc[self.cc0]
    cc_by_cell = self.maze.connected_component_by_cell()
    
    while exits_from_cc0:
      # print self.maze
      # print self.laplacian
      # print "rmin=%d, rmax=%d" % (rmin, rmax)
      
      x,y,d = exits_from_cc0.pop(0)
      neighbouring_cc = cc_by_cell[(x,y)]
      if neighbouring_cc == self.cc0:
        # print "LOOP!"
        continue
      
      index = self.index_by_cc[neighbouring_cc]
      self.laplacian[index,index] -= 1
      num_without_exit = det(self.laplacian)
      
      # print "There are %d completions without the passage (%d, %d, %d)" % (num_without_exit, x,y,d)
      
      if i < rmin + num_without_exit:
        rmax = rmin + num_without_exit
      else:
        rmin += num_without_exit
        self.laplacian[index,index] += 1
        
        # incorporate exits from the component we've newly connected to
        for ox,oy,od in self.exits_by_cc[neighbouring_cc]:
          if cc_by_cell[(ox,oy)] != self.cc0:
            exits_from_cc0.append((ox,oy,od))
        
        # Update the laplacian matrix
        for j in range(len(self.laplacian)):
          if j == index:
            self.laplacian[j,j] = 1
          else:
            self.laplacian[index,j] = self.laplacian[j,index] = 0
        
        # Add the passage to the maze
        self.maze.carve(x,y,d)
    
    return self.maze
  
  def __len__(self):
    return self.n
  
  def __getitem__(self, i):
    if not 0 <= i < self.n:
      raise IndexError("maze index out of range")
    return self.nth_completion(i)
