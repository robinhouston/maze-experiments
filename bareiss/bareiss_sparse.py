# Using an even more economical representation of symmetric matrices,
# where we just record the inhabited stripe of the lower triangle.

# If the stripe width is s, then row i is missing the first max(i-s,0) elements.

class SSM(object):
  class Row(object):
    def __init__(self, ssm, x):
      self.ssm, self.x = ssm, x
    def __getitem__(self, y):
      assert 0 <= y < self.ssm.n
      return self.ssm.a[x * self.ssm.n + y]
    def __setitem__(self, y, v):
      assert 0 <= y < self.ssm.n
      self.ssm.a[x * self.ssm.n + y] = v
  def __init__(self, n, s):
    self.n, self.s = n, s
    self.a = [0] * (n*n)
  def __getitem__(self, x):
    assert 0 <= x < self.n
    return self.Row(self, x)

def lap(width, height):
  """Laplacian matrix of a width x height grid.
  """
  n = width * height
  m = [ [0] * (min(i,width) + 1) for i in range(n) ]
  for i in range(n):
    if i % width:
      m[i][min(i, width) - 1] = -1
  for i in range(width, n):
    m[i][0] = -1
  for i in range(n):
    ii = min(i, width)
    for j in range(ii):
      m[i][ii] -= m[i][j]
      m[j+i-ii][-1] -= m[i][j]
  return m

def bareiss(m):
  """Perform the Bareiss algorithm on the matrix.
  """
  import copy
  m = copy.deepcopy(m)
  n, s = len(m), len(m[-1])-1
  for k in range(n-1):
    for i in range(k+1, n):
      di = max(i-s, 0)
      for j in range(max(k+1, i-s), i+1):
        dj = max(j-s, 0)
#        print "%d, %d, %d" % (i,j,k)
        m[i][j - di] *= m[k][-1]
        if k >= di:
          m[i][j - di] -= m[i][k - di] * m[j][k - dj]
        if k > 0:
          m[i][j - di] //= m[k-1][-1]
#    print m
  return m

def det(m):
  return bareiss(m)[-1][-1]

def n_mazes(width, height):
  return det(lap(width, height)[:-1])
