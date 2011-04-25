def lap(width, height):
  """Laplacian matrix of a width x height grid.
  """
  n = width * height
  m = [ [0] * n for i in range(n) ]
  for i in range(n):
    if i % width:
      m[i-1][i] = m[i][i-1] = -1
  for i in range(n-width):
    m[i][i+width] = m[i+width][i] = -1
  for i in range(n):
    m[i][i] = -sum(m[i])
  return m

def lap(width, height):
  """Laplacian matrix of a width x height grid.
  """
  n = width * height
  m = [ [0] * n for i in range(n) ]
  for i in range(n):
    if i % width:
      m[i-1][i] = m[i][i-1] = -1
  for i in range(n-width):
    m[i][i+width] = m[i+width][i] = -1
  for i in range(n):
    m[i][i] = -sum(m[i])
  return m


def bareiss(m):
  """Perform the Bareiss algorithm on the matrix.
  """
  import copy
  m = copy.deepcopy(m)
  n = len(m)
  for k in range(n-1):
    for i in range(k+1, n):
      for j in range(k+1, n):
        m[i][j] = m[i][j] * m[k][k] - m[i][k] * m[k][j]
        if k > 0:
          m[i][j] //= m[k-1][k-1]
  return m

def det(m):
  return bareiss(m)[-1][-1]

def sm(m, k):
  return [ row[:k] for row in m[:k] ]
