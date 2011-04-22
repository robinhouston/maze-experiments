

# Each cell can have up to four exits, and each of these
# can be either a normal exit (N, E, S, W) or an "under"
# weave underneath the adjacent cell (UN, UE, US, UW).
#
# So really the cell value should be a four-digit number
# in ternary - but it's simpler to stick with binary and
# use two bits for each notional trit. Note that some
# combinations are forbidden: value & (value >> 4) == 0
# is the invariant.
N, E, S, W = 0x01, 0x02, 0x04, 0x08
UN, UE, US, UW = 0x10, 0x20, 0x40, 0x80
NON_U_MASK, U_MASK = 0x0F, 0xF0

DIRECTION_LIST = [N, E, S, W]
DIRECTIONS = set(DIRECTION_LIST)
DELTA = {N:(0,-1), E:(1,0), S:(0,1), W:(-1,0)}
DELTA_R = {(0,-1):N, (1,0):E, (0,1):S, (-1,0):W}
OPPOSITE = {N:S, E:W, S:N, W:E}
CLOCKWISE = {N:E, E:S, S:W, W:N}
ANTICLOCKWISE = {N:W, W:S, S:E, E:N}

def random_direction():
  import random
  return random.choice(DIRECTION_LIST)

class _RelativeDirection(object):
  """Represents a relative direction.
  There are four instances: LEFT, AHEAD, RIGHT, and BACK.
  """
  def __init__(self, name, f_abs):
    self.name = name
    self.f_abs = f_abs
  def abs(self, direction):
    assert direction in DIRECTIONS
    return self.f_abs(direction)
  def __str__(self):
    return self.name

LEFT = _RelativeDirection("LEFT", lambda d: ANTICLOCKWISE[d])
AHEAD = _RelativeDirection("AHEAD", lambda d: d)
RIGHT = _RelativeDirection("RIGHT", lambda d: CLOCKWISE[d])
BACK = _RelativeDirection("BACK", lambda d: OPPOSITE[d])

RELATIVE_DIRECTIONS = [LEFT, AHEAD, RIGHT]

H_OVER_V, V_OVER_H = object(), object()

def _invert_U(value):
  assert 0 <= value <= 0xFF
  return ((value & 0xF) << 4) | (value >> 4)

class _ConnectedComponent(object):
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
    if self != other:
      self._root()._parent = other
  
  def __eq__(self, other):
    return self._root()._id == other._root()._id
  def __ne__(self, other):
    return self._root()._id != other._root()._id
  def __hash__(self):
    return hash(self._root()._id)

class Col(object):
  def __init__(self, num_rows):
    self.num_rows = num_rows
    self._cells = [0] * num_rows
  def __getitem__(self, y):
    return self._cells[y]
  def __setitem__(self, y, v):
    assert v & (v >> 4) == 0
    self._cells[y] = v

class Maze(object):
  def __init__(self, num_cols, num_rows, cursor=(0, 0, E)):
    self.num_cols = num_cols
    self.num_rows = num_rows
    self.cols = [ Col(num_rows) for x in range(num_cols) ]
    self.cursor_col, self.cursor_row, self.cursor_dir = cursor
    self._components = None
    self.weaves = set()
    self.num_nonempty_cells = 0
  
  # Cells and their values
  
  def __getitem__(self, x):
    return self.cols[x]
  
  def cells(self):
    for x in range(self.num_cols):
      for y in range(self.num_rows):
        yield x, y
  
  # Cursor manipulation
  
  def cursor(self):
    return (self.cursor_col, self.cursor_row, self.cursor_dir)
  
  def cursor_cell(self):
    return (self.cursor_col, self.cursor_row)
  
  def move(self, *move_spec):
    if len(move_spec) == 1:
      direction, = move_spec
      direction = self._abs(direction)
      return self.turn(direction).move_rel(*DELTA[direction])
    elif len(move_spec) == 2:
      x, y = move_spec
      if not (0 <= x < self.num_cols and 0 <= y < self.num_rows):
        return False
      self.cursor_col, self.cursor_row = x, y
    elif len(move_spec) == 3:
      x, y, direction = move_spec
      if not (0 <= x < self.num_cols and 0 <= y < self.num_rows):
        return False
      self.cursor_col, self.cursor_row, self.cursor_dir = x, y, self._abs(direction)
    else:
      raise ValueError("move() takes 1, 2 or 3 arguments (%d given)" % len(move_spec))
    
    return True
  
  def move_rel(self, dx, dy):
    return self.move(self.cursor_col + dx, self.cursor_row + dy)
  
  def _abs(self, direction):
    if isinstance(direction, _RelativeDirection):
      return direction.abs(self.cursor_dir)
    elif direction in DIRECTIONS:
      return direction
    else:
      raise ValueError("Bad direction: %r" % (direction,))
  
  def turn(self, direction):
    self.cursor_dir = self._abs(direction)
    return self
  
  
  # Carving passages
  
  def _add(self, x, y, v_add, v_remove=0, do_not_override=False):
    v = self[x][y]
    if do_not_override:
      v_add = v_add & ~_invert_U(v)
    v = (v & ~_invert_U(v_add) | v_add) & ~(v_remove | _invert_U(v_remove))
    self._set(x, y, v)
  
  def _set(self, x, y, v):
    prev = self[x][y]
    if prev == 0 and v != 0:
      self.num_nonempty_cells += 1
    elif prev != 0 and v == 0:
      self.num_nonempty_cells -= 1
    
    self[x][y] = v
  
  def carve(self, *args):
    if len(args) == 1:
      direction, = args
      self.cursor_dir = self._abs(direction)
      r = self._carve(self.cursor_col, self.cursor_row, self.cursor_dir)
      if r:
        self.cursor_col, self.cursor_row = r
        return True
      else:
        return False
    elif len(args) == 2:
      (sx, sy), (tx, ty) = args
      direction = DELTA_R[(tx-sx, ty-sy)]
      return bool(self._carve(sx, sy, direction))
    elif len(args) == 3:
      x, y, direction = args
      return bool(self._carve(x, y, self._abs(direction)))
    else:
      raise TypeError("carve() takes 1, 2 or 3 arguments (%d given)" % len(args))
  
  def _carve(self, x, y, direction, **kwargs):
    if not (0 <= x < self.num_cols and 0 <= y < self.num_rows):
      raise ValueError("carve(): position (%d,%d) is out of bounds" % (x, y))
    
    dx, dy = DELTA[direction]
    tx, ty = x + dx, y + dy
    if not (0 <= tx < self.num_cols and 0 <= ty < self.num_rows):
      return ()
    
    self._add(x, y, direction)
    self._add(tx, ty, OPPOSITE[direction])
    
    if self._components is not None:
      self._components[(x,y)].identify_with(self._components[(tx,ty)])
    
    return tx, ty
  
  def carve_path(self, path):
    for i in range(len(path) - 1):
      self.carve(path[i], path[i+1])
  
  def weave(self, x, y, weave_type):
    if not (0 < x < self.num_cols-1 and 0 < y < self.num_rows-1):
      raise ValueError("weave(): position (%d,%d) is out of bounds" % (x, y))
    if weave_type not in (H_OVER_V, V_OVER_H):
      raise ValueError("weave(): unknown weave_type")
    
    # Adding a weave in a cell that has exits already can cause
    # previously connected passages to become disconnected.
    if self._components is not None and self[x][y] != 0:
      self._components = None
    
    if self._components is not None:
      c = self._components
      c[(x-1, y)].identify_with(c[(x+1, y)])
      c[(x, y-1)].identify_with(c[(x, y+1)])
      if weave_type == H_OVER_V:
        c[(x, y)].identify_with(c[(x-1, y)])
      else:
        c[(x, y)].identify_with(c[(x, y-1)])
    
    self._set(x, y, {H_OVER_V: UN|E|US|W, V_OVER_H: N|UE|S|UW}[weave_type])
    
    self._add(x, y-1, S, do_not_override=True)
    self._add(x+1, y, W, do_not_override=True)
    self._add(x, y+1, N, do_not_override=True)
    self._add(x-1, y, E, do_not_override=True)
    
    self.weaves.add((x, y, weave_type))
  
  # Inspection
  
  def has_exit(self, direction, under=False):
    d = self._abs(direction)
    if under:
      d = d << 4
    
    return self[self.cursor_col][self.cursor_row] & d != 0
  
  def cell_is_empty(self, *args):
    if len(args) == 1:
      direction, = args
      dx, dy = DELTA[self._abs(direction)]
      x, y = self.cursor_col + dx, self.cursor_row + dy
    elif len(args) == 2:
      x, y = args
    else:
      raise ValueError("cell_is_empty() takes 1 or 2 arguments (%d given)" % len(args))
  
    if not (0 <= x < self.num_cols and 0 <= y < self.num_rows):
      return None
  
    return 0 == self[x][y]
  
  def has_empty_cells(self):
    return self.num_nonempty_cells < self.num_rows * self.num_cols
  
  def _init_components(self):
    self._components = c = dict((
      ((x,y), _ConnectedComponent())
      for x in range(self.num_cols)
      for y in range(self.num_rows)
    ))
    
    for sx, sy, d in self.corridors():
      dx, dy = DELTA[d]
      tx, ty = sx+dx, sy+dy
      c[(sx,sy)].identify_with( c[(tx,ty)])
    
    for x, y, weave_type in self.weaves:
      c[(x-1, y)].identify_with(c[(x+1, y)])
      c[(x, y-1)].identify_with(c[(x, y+1)])
      if weave_type == H_OVER_V:
        c[(x, y)].identify_with(c[(x-1, y)])
      else:
        c[(x, y)].identify_with(c[(x, y-1)])
  
  def is_connected(self, *args):
    if len(args) == 2:
      c1, c2_or_d = args
    elif len(args) == 3:
      x, y, c2_or_d = args
      c1 = (x, y)
    elif len(args) == 4:
      sx,sy, tx,ty = args
      c1, c2_or_d = (sx,sy), (tx,ty)
    
    if isinstance(c2_or_d, _RelativeDirection) or c2_or_d in DIRECTIONS:
      x, y = c1
      dx, dy = DELTA[self._abs(c2_or_d)]
      c2 = (x + dx, y + dy)
    else:
      c2 = c2_or_d
    
    if self._components is None:
      self._init_components()
    return self._components[c1] == self._components[c2]
  
  def doorways(self):
    for x in range(self.num_cols):
      for y in range(self.num_rows):
        if x < self.num_cols - 1:
          yield x, y, E
        if y < self.num_rows - 1:
          yield x, y, S
  
  def walls(self):
    for x, y, d in self.doorways():
      if self[x][y] & (d | _invert_U(d)) == 0:
        yield x, y, d
  
  def corridors(self):
    for x, y, d in self.doorways():
      dx, dy = DELTA[d]
      if self[x][y] & d != 0 and self[x+dx][y+dy] & OPPOSITE[d] != 0:
        yield x, y, d
  
  # Transactions and branching
  
  def transaction(self):
    return MazeTransaction(self)
  
  def branch(self, directions):
    for direction in directions:
      cursor = self.cursor()
      yield direction
      self.move(*cursor)
  
  
  # Rendering
  
  def render_as_unicode(self):
    import mazer.render
    return mazer.render.UnicodeRenderer(self).render()

def MazeTransaction(object):
  def __init__(self, maze):
    self.maze = maze
  
  def __enter__(self):
    self.cursor = self.maze.cursor
    self.v = [ list(col) for col in self.maze ]
    self.weaves = set(self.maze.weaves)
    self.num_nonempty_cells = self.maze.num_nonempty_cells
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    if exc_type is not None:
      self.rollback()
  
  def rollback(self):
    self.maze.move(*self.cursor)
    for x, row in enumerate(self.v):
      for y, v in enumerate(row):
        self.maze[x][y] = v
    self.maze.weaves = self.weaves
    self.maze._components = None
    self.maze.num_nonempty_cells = self.num_nonempty_cells
