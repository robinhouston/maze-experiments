import re

def c(s, w):
  left_padding = (w - len(s)) / 2
  right_padding = w - left_padding - len(s)
  return " " * left_padding + s + " " * right_padding

def symgen():
  s = ""
  while True:
    if re.match(r"^z*$", s):
      s = "a" * (1 + len(s))
    else:
      s = re.sub(r"(.)(z*)$", lambda mo: chr(1 + ord(mo.group(1))) + "a" * len(mo.group(2)), s)
    yield s

default_symgen = symgen()

class Ex(object):
  """Represents an algebraic expression.
  """
  def __ne__(self, other):
    return not (self == other)
  def __hash__(self):
    return hash(repr(self))
  def __add__(self, other):
    s = SumEx([self, other])
    if len(s.exprs) == 1:
      return s.exprs[0]
    return s
  def __radd__(self, other):
    if other == 0:
      return self
    elif self == ZERO:
      return other
    else:
      print self, other
      return NotImplemented
  def __mul__(self, other):
    if self == ZERO or other == ZERO or other == 0:
      return ZERO
    if other == 1:
      return self
    if other == -1:
      return -self
    return ProdEx([self, other])
  def __rmul__(self, other):
    if other == 0:
      return ZERO
    if other == 1:
      return self
    if other == -1:
      return -self
    return NotImplemented
  def __neg__(self):
    if isinstance(self, NegEx):
      return self.expr
    elif isinstance(self, SumEx):
      return SumEx([-x for x in self.exprs])
    else:
      return NegEx(self)
  def __sub__(self, other):
    return self + (-other)

class ConstantEx(Ex):
  def __init__(self, symbol=None):
    if symbol is None:
      symbol = default_symgen.next()
    self.symbol = symbol
  def __eq__(self, other):
    return isinstance(other, ConstantEx) and self.symbol == other.symbol
  def __str__(self):
    return self.symbol
  def __repr__(self):
    return "ConstantEx('%s')" % self.symbol

class _ListEx(Ex):
  def __init__(self, exprs):
    self.exprs = []
    self.extend(exprs)
  def __eq__(self, other):
    return isinstance(other, SumEx) and self.exprs == other.exprs
  def extend(self, exprs):
    for expr in exprs:
      self.append(expr)

class SumEx(_ListEx):
  def append(self, expr):
    if isinstance(expr, SumEx):
      return self.extend(expr.exprs)
    if isinstance(expr, NegEx):
      if expr.expr in self.exprs:
        self.exprs.remove(expr.expr)
        return
    elif NegEx(expr) in self.exprs:
      self.exprs.remove(NegEx(expr))
      return
    elif expr == 0:
      return
    return self.exprs.append(expr)
  def __str__(self):
    if not self.exprs:
      return "0"
    else:
      return "(%s)" % (" + ".join(map(str, self.exprs)))
  def __repr__(self):
    if not self.exprs:
      return "SumEx([])"
    elif len(self.exprs) == 1:
      return "SumEx([%s])" % (repr(self.exprs[0]),)
    else:
      return "(%s)" % (" + ".join(map(repr, self.exprs)))

class NegEx(Ex):
  def __init__(self, expr):
    self.expr = expr
  def __eq__(self, other):
    return isinstance(other, NegEx) and self.expr == other.expr
  def __str__(self):
    return "-(%s)" % str(self.expr)
  def __repr__(self):
    return "NegEx(%s)" % (repr(self.expr),)

ZERO = SumEx([])

class ProdEx(_ListEx):
  def append(self, expr):
    if isinstance(expr, ProdEx):
      self.extend(expr.exprs)
    else:
      self.exprs.append(expr)
  def __div__(self, other):
    if other in self.exprs:
      remaining_exprs = [ e for e in self.exprs ]
      remaining_exprs.remove(other)
      if len(remaining_exprs) == 1:
        return remaining_exprs[0]
      else:
        return ProdEx(remaining_exprs)
    return super(ProdEx, self).__div__(other)
  def __str__(self):
    if not self.exprs:
      return "1"
    else:
      return "(%s)" % ("*".join(map(str, self.exprs)))
  def __repr__(self):
    if not self.exprs:
      return "ProdEx([])"
    elif len(self.exprs) == 1:
      return "ProdEx([%s])" % (repr(self.exprs[0]),)
    else:
      return "(%s)" % (" * ".join(map(repr, self.exprs)))

ONE = ProdEx([])

class Matrix(object):
  def __init__(self, num_rows, num_cols):
    self.num_rows = num_rows
    self.num_cols = num_cols
    self.m = [ [None] * num_cols for i in range(num_rows) ]
  def __getitem__(self, row):
    return self.m[row]
  def __str__(self):
    return "\n".join([ " ".join([ c(str(x), 13) for x in row ]) for row in self.m ])
  def set(self, m):
    for r in range(self.num_rows):
      for c in range(self.num_cols):
        self[r][c] = m[r][c]
  
  def mv_det(self, start_pos=0):
    """Compute the determinant of the matrix, using the Mahajan-Vinay algorithm."""
    v = None
    for i in range(self.num_cols - 1, start_pos - 1, -1):
      v = self.mv_vector(i, v)
      print i
    return v[-1]
  
  @staticmethod
  def dot_prod(v, w):
    return sum([ a * b for a, b in zip(v, w) ])

  def mv_vector(self, start_pos=0, prev_vector=None):
    assert self.num_rows == self.num_cols
    assert start_pos < self.num_cols
  
    # This function just implements equation (7) from
    # http://page.mi.fu-berlin.de/rote/Papers/pdf/Division-free+algorithms.pdf
    #
    # Our mult_row vector is equal, successively, to the rows of the
    # self in that equation; our rM_row is equal, successively, to
    # r, rM, rMM, etc.
  
    if start_pos == self.num_cols - 1:
      return [ -1, self[start_pos][start_pos] ]
    
    if prev_vector is None:
      prev_vector = self.mv_vector(start_pos+1)
    our_vector = [None] * (1 + len(prev_vector))
  
    mult_row = [-1] + [0] * (len(prev_vector) - 1)
    rM_row = self[start_pos][start_pos+1:]
    s_col = [ self[r][start_pos] for r in range(start_pos+1, self.num_rows) ]
    M_cols = [
      [ self[r][c] for r in range(start_pos+1, self.num_rows) ]
      for c in range(start_pos+1, self.num_cols)
    ]
  
    for i in range(len(prev_vector) + 1):
      #print "mult_row: %s" % mult_row
      our_vector[i] = self.dot_prod(mult_row, prev_vector)
    
      if i == 0:
        mult_row = [self[start_pos][start_pos]] + mult_row[:-1]
      else:
        mult_row = [self.dot_prod(rM_row, s_col)] + mult_row[:-1]
        #print "Applying M_cols = %s" % (M_cols,)
        rM_row = [ self.dot_prod(rM_row, M_col) for M_col in M_cols ]
  
    return our_vector

class Graph(object):
  def __init__(self, num_nodes):
    self.num_nodes = num_nodes
    self.edges = {}
    self.symgen = symgen()
  
  def add_edge(self, n1, n2, val=None):
    if n1 > n2:
      return self.add_edge(n2, n1, val)
    if val is None:
      val = ConstantEx(self.symgen.next())
    assert isinstance(val, Ex)
    self.edges.setdefault(n1, {})[n2] = val
  
  def get_edge(self, n1, n2):
    if n1 > n2:
      return self.get_edge(n2, n1)
    return self.edges.get(n1, {}).get(n2, ZERO)
  
  def matrix(self):
    m = Matrix(self.num_nodes, self.num_nodes)
    for n2 in range(self.num_nodes):
      m[n2][n2] = ZERO
      for n1 in range(self.num_nodes):
        if n1 != n2:
          edge = self.get_edge(n1, n2)
          m[n1][n2] = -edge
          m[n2][n2] += edge
    return m

def grid(rows, cols):
  """Compute the algebraic Laplacian matrix for the grid graph.
  """
  g = Graph(rows * cols)
  for y in range(rows):
    for x in range(cols - 1):
      g.add_edge(y * cols + x, y * cols + x + 1)
    if y < rows - 1:
      for x in range(cols):
        g.add_edge(y * cols + x, (y+1) * cols + x)
  
  return g.matrix()


a = ConstantEx("a")
b = ConstantEx("b")

m2 = Matrix(2,2)
m2.set([
  [ConstantEx("a"), ConstantEx("b")],
  [ConstantEx("c"), ConstantEx("d")],
])

m3 = Matrix(3,3)
m3.set([
  [0, ConstantEx("x"), 0],
  [ConstantEx("a"), 0, ConstantEx("b")],
  [ConstantEx("c"), 0, ConstantEx("d")]
])

# m3 = Matrix(3,3)
# m3.set([
#   [ConstantEx("v"), ConstantEx("w"), ConstantEx("x"),],
#   [ConstantEx("y"), ConstantEx("a"), ConstantEx("b")],
#   [ConstantEx("z"), ConstantEx("c"), ConstantEx("d")]
# ])
