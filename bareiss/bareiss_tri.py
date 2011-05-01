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

def lap_co(width, height, x=4):
  w, h = width - 1, height - 1
  n = w * h
  m = [ [0] * (i+1) for i in range(n) ]
  for i in range(n):
    m[i][i] = x
    if i % w:
      m[i][i-1] = -1
    if i + w < n:
      m[i+w][i] = -1
  return m

def bareiss(m):
  """Perform the Bareiss algorithm on the matrix.
  """
  # import copy
  # m = copy.deepcopy(m)
  n = len(m)
  for k in range(n-1):
    for i in range(k+1, n):
      for j in range(k+1, i+1):
        m[i][j] = m[i][j] * m[k][k] - m[i][k] * m[j][k]
        if k > 0:
          m[i][j] /= m[k-1][k-1]
  return m

def det(m):
  return bareiss(m)[-1][-1]

def n_mazes(width, height):
  return det(lap(width, height)[:-1])



def zero(n):
  return [ [0] * (i+1) for i in range(n) ]

def ident(n):
  return [ [0] * i + [1] for i in range(n) ]

def mobki(n, k):
  """Minus-one-bordered k-times-identity.
  """
  m = zero(n)
  for i in range(n):
    m[i][i] = k
    if i > 0: m[i][i-1] = -1
  return m


def multiply(m1, m2):
  assert len(m1) == len(m2)
  n = len(m1)
  result = zero(n)
  for i in range(n):
    for j in range(i+1):
      for k in range(n):
        result[i][j] += m1[max(i,k)][min(i,k)] * m2[max(j,k)][min(j,k)]
  return result

def add(m1, m2):
  assert len(m1) == len(m2)
  return [
    [ m1[i][j] + m2[i][j]  for j in range(i+1) ]
    for i in range(len(m1))
  ]

def subtract(m1, m2):
  assert len(m1) == len(m2)
  return [
    [ m1[i][j] - m2[i][j]  for j in range(i+1) ]
    for i in range(len(m1))
  ]

def minus(m):
  return [ [ -x for x in row ] for row in m ]

def bits(n):
  """Represent an integer as an array of binary digits.
  """
  bits = []
  while n > 0:
    n, bit = divmod(n, 2)
    bits.append(bit)
  bits.reverse()
  return bits

def dmf(m, k):
  n = len(m)
  a, b, c = minus(ident(n)), zero(n), ident(n)
  for bit in bits(k):
    a, b = subtract(multiply(b,b), multiply(a,a)), subtract(multiply(b, c), multiply(a, b))
    if bit: a, b = b, subtract(multiply(b, m), a)
    c = subtract(multiply(b, m), a)
  return b

def n_mazes_(width, height):
  return det( dmf(mobki(width-1, 4), height) )
