# Using a more economical representation of symmetric matrices,
# where we just record the lower triangle.

def lap(width, height):
  """Laplacian matrix of a width x height grid.
  """
  n = width * height
  m = [ [0] * (i+1) for i in range(n) ]
  for i in range(n):
    if i % width:
      m[i][i-1] = -1
  for i in range(n-width):
    m[i+width][i] = -1
  for i in range(n):
    for j in range(i):
      m[i][i] -= m[i][j]
      m[j][j] -= m[i][j]
  return m

def bareiss(m):
  """Perform the Bareiss algorithm on the matrix.
  """
  import copy
  m = copy.deepcopy(m)
  n = len(m)
  for k in range(n-1):
    for i in range(k+1, n):
      for j in range(k+1, i+1):
        m[i][j] = m[i][j] * m[k][k] - m[i][k] * m[j][k]
        if k > 0:
          m[i][j] //= m[k-1][k-1]
  return m

def det(m):
  return bareiss(m)[-1][-1]

def n_mazes(width, height):
  return det(lap(width, height)[:-1])
