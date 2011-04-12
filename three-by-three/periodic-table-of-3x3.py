# Make a PDF file containing all the 3x3 weave mazes, on a 16 x 16 grid.
# The file is output as "all-the-3x3-weave-mazes.pdf".

import cairo

C = 20 # cell size
B = 15 # border size
G = 6  # gap size for bridges

MARGIN = 120
GAP_BETWEEN_CELLS = 40

PAGE_SIZE_PTS = 6 * 72

FILL_COLOUR = (.86, .2, .2)
STROKE_COLOUR = None #(.4, .1, .1)

logical_dimen = MARGIN + 16 * (C+B+C+B+C) + 15 * GAP_BETWEEN_CELLS + MARGIN

def branch(e, matrix=None, bridge_gap=False):
  if matrix is not None:
    c.save()
    c.transform(matrix)
    b = branch(e, bridge_gap=bridge_gap)
    c.restore()
    return b
  
  if bridge_gap:
    path = [(B+C+B, B+C+B-G)]
  else:
    path = [( B+C+B, B+C+B )]
  c.move_to(*path[0])
  def rel_to(x, y):
    c.rel_move_to(x, y)
    path.append(c.get_current_point())
  def to(x, y):
    c.move_to(x, y)
    path.append(c.get_current_point())
  
  if e:
    to( B+C+B, B+C )
    if e[0]:
      if e[0] == 1:
        to( B, B+C )
      else:
        rel_to( -B, 0 )
        if e[0] == 2:
          rel_to( 0, B+C )
          rel_to( -C, 0 )
        elif e[0] == -1:
          rel_to( 0, B )
          rel_to( B-G, 0 )
          rel_to( 0, C )
          rel_to( G-B, 0 )
          rel_to( -C, 0 )
        else:
          if e[0] == 3:
            rel_to( 0, B+C+B+C )
            rel_to( -C, 0 )
          elif e[0] == -2:
            rel_to( 0, B )
            rel_to( B-G, 0 )
            rel_to( 0, C )
            rel_to( G-B, 0 )
            rel_to( 0, B+C )
            rel_to( -C, 0 )
          else:
            rel_to( 0, B+C+B )
            if e[0] == 4:
              rel_to( B+C, 0 )
              rel_to( 0, C )
            else:
              if e[0] == 5:
                rel_to( B+C+B+C, 0 )
                rel_to( 0, C )
              else:
                rel_to( B+C+B, 0)
                if e[0] == 6:
                  rel_to( 0, -B-C )
                  rel_to( C, 0 )
                else:
                  rel_to( 0, -B-C-B-C )
                  rel_to( C, 0 )
              to( B+C+B+C+B+C, B+C+B+C+B+C)
          to( B, B+C+B+C+B+C )
      to(B, B)
    else:
      rel_to( 0, -C )
    
    to( B+C+B+C, B )
    if e[1]:
      rel_to( B+C, 0 )
      if e[1] == 1:
        rel_to( 0, C )
        rel_to( -C-B, 0 )
      else:
        if e[1] == 2:
          rel_to( 0, C+B+C )
          rel_to( -C, 0 )
        elif e[1] == -1:
          rel_to( 0, C+B+C )
          rel_to( -C-B+G, 0 )
          rel_to( 0, -C )
          rel_to( B-G, 0 )
        else:
          rel_to( 0, C+B+C+B+C )
          if e[1] == 3 or e[1] == -2:
            rel_to( -C, 0 )
          else:
            if e[1] == 4:
              rel_to( -C-B-C, 0 )
              rel_to( 0, -C )
            else:
              to( B, B+C+B+C+B+C )
              if e[1] == 5:
                rel_to( 0, -C )
              else:
                if e[1] == 6:
                  rel_to( 0, -C-B-C )
                else:
                  rel_to( 0, -C-B-C-B-C )
                rel_to( C, 0 )
                to( B+C, B+C+B+C+B )
            to( B+C+B+C+B, B+C+B+C+B )
        if e[1] == -2:
          to( B+C+B+C+B, B+C+B+C )
          rel_to( G-B, 0 )
          rel_to( 0, -C )
          rel_to( B-G, 0 )
          rel_to( 0, -B )
        else:
          to( B+C+B+C+B, B+C )
    
    to( B+C+B+C, B+C )
    if bridge_gap:
      rel_to( 0, B-G )
    else:
      rel_to( 0, B )
  else:
    rel_to( C, 0 )
  
  return [ c.user_to_device(*p) for p in path ]

EPSILON = 1E-2
def pt_equal(p1, p2):
  return (-EPSILON < p1[0] - p2[0] < +EPSILON) \
     and (-EPSILON < p1[1] - p2[1] < +EPSILON)

def join_branches(*branches):
  branch_end = None
  for branch in branches:
    if branch_end is not None:
      this_branch_start = branch.pop(0)
      if not pt_equal(this_branch_start, branch_end):
        raise Exception("Branch matching fail: %s != %s" % (branch_end, this_branch_start))
    for p in branch:
      yield p
    branch_end = branch[-1]

def draw(path):
  path_iter = iter(path)
  
  c.save()
  scale_factor = float(PAGE_SIZE_PTS) / logical_dimen
  c.scale(scale_factor, scale_factor)

  c.move_to(*path_iter.next())
  for x,y in path_iter:
    c.line_to(x,y)
  c.close_path()
  
  if FILL_COLOUR:
    c.set_source_rgb(*FILL_COLOUR)
    if STROKE_COLOUR:
      c.fill_preserve()
    else:
      c.fill()
  if STROKE_COLOUR:
    c.set_source_rgb(*STROKE_COLOUR)
    c.stroke()
  
  c.restore()

MR = cairo.Matrix(0,1, -1,0, B+C+B+C+B+C+B,0)
MB = cairo.Matrix(-1,0, 0,-1, B+C+B+C+B+C+B,B+C+B+C+B+C+B)
ML = cairo.Matrix(0,-1, 1,0, 0,B+C+B+C+B+C+B)

class cell(object):
  def __init__(self, cell_row, cell_col):
    self.cell_row = cell_row
    self.cell_col = cell_col
  def __enter__(self):
    c.save()
    c.translate(
      MARGIN + (C+B+C+B+C+GAP_BETWEEN_CELLS) * self.cell_col - B,
      MARGIN + (C+B+C+B+C+GAP_BETWEEN_CELLS) * self.cell_row - B,
    )
  def __exit__(self, _t, _v, _tr):
    c.restore()

def maze(cell_row, cell_col, maze_spec):
  with cell(cell_row, cell_col):
    t, r, b, l = maze_spec
    br_t = branch(t)
    br_r = branch(r, MR)
    br_b = branch(b, MB)
    br_l = branch(l, ML)
  
  return join_branches(br_t, br_r, br_b, br_l)

def draw_maze(*args, **kwargs):
  return draw(maze(*args, **kwargs))

def draw_branch(cell_row, cell_col, *args, **kwargs):
  with cell(cell_row, cell_col):
    b = branch(*args, **kwargs)
  draw(b)

def draw_mazes():
  for i in range(8):
    draw_maze(15, 4+i, ((i,7-i), (), (), ()))
    draw_maze(4+i, 0, ((), (7-i,i), (), ()))
    draw_maze(0, 4+i, ((), (), (7-i,i), ()))
    draw_maze(4+i, 15, ((), (), (), (i,7-i)))
  
  for i in range(4):
    for j in (0,1):
      draw_maze(4*(j+1) + i, 3, ((i, 3-j), (), (j, 3-i), ()))
      draw_maze(3, 11 - 4*j - i, ((), (i, 3-j), (), (j, 3-i)))
    for j in (2,3):
      draw_maze(4*(j-1) + i, 12, ((i, 3-j), (), (j, 3-i), ()))
      draw_maze(12, 19 - 4*j - i, ((), (i, 3-j), (), (j, 3-i)))
  
  def corner_pos(i, j):
    if j < 4:
      return 4+i, 8+j
    else:
      return 6+i, 6+j
  for i in range(2):
    for j in range(6):
      row, col = corner_pos(i, j)
      draw_maze( row, col, ((j,i), (1-i,5-j), (), ()) )
      draw_maze( 15-row, col, ((), (5-j,1-i), (i,j), ()) )
      draw_maze( row, 15-col, ((i,j), (), (), (5-j,1-i)) )
      draw_maze( 15-row, 15-col, ((), (), (j,i), (1-i,5-j)) )
  
  for i in range(2):
    for j in range(2):
      for k in range(4):
        draw_maze(1+i, 4+4*j+k, ((i,j),(1-j,k),(),(3-k,1-i)))
        draw_maze(4+4*j+k, 14-i, ((3-k,1-i),(i,j),(1-j,k),()))
        draw_maze(14-i, 4+4*j+k, ((),(k,1-j),(j,i),(1-i,3-k)))
        draw_maze(4 + 4*j + k, 1+i, ((1-i,3-k),(),(k,1-j),(j,i)))
  
  for i in range(4):
    for j in range(4):
      draw_maze(6+i, 6+j, (
        ((i&2)/2, i%2),
        (1 - i%2, j%2),
        (1 - j%2, (j&2)/2),
        (1 - (j&2)/2, 1 - (i&2)/2)
      ))
  
  for i in (0,1):
    for j in (0,1):
      for k in (0,1):
        draw_maze(i, 2*j+k, ((k-2,i),(),(1-j,k),()))
        draw_branch(i, 2*j+k, (1-i, j), matrix=MR, bridge_gap=True)
        draw_maze(i+2, 2*j+k, ((),(1-i,j),(),(1-k,-1-i)))
        draw_branch(i+2, 2*j+k, (1-j, k), matrix=MB, bridge_gap=True)
        
        draw_maze(i, 15-2*j-k, ((i,k-2),(),(k,1-j),()))
        draw_branch(i, 15-2*j-k, (j, 1-i), matrix=ML, bridge_gap=True)
        draw_maze(i+2, 15-2*j-k, ((),(-1-i,1-k),(),(j,1-i)))
        draw_branch(i+2, 15-2*j-k, (k, 1-j), matrix=MB, bridge_gap=True)
        
        draw_maze(15-i, 2*j+k, ((k,1-j),(),(i,k-2),()))
        draw_branch(15-i, 2*j+k, (j, 1-i), matrix=MR, bridge_gap=True)
        draw_maze(13-i, 2*j+k, ((),(j,1-i),(),(-1-i,1-k)))
        draw_branch(13-i, 2*j+k, (k, 1-j), matrix=None, bridge_gap=True)
        
        draw_maze(15-i, 15-2*j-k, ((1-j,k),(),(k-2,i),()))
        draw_branch(15-i, 15-2*j-k, (1-i, j), matrix=ML, bridge_gap=True)
        draw_maze(13-i, 15-2*j-k, ((),(1-k,-1-i),(),(1-i,j)))
        draw_branch(13-i, 15-2*j-k, (1-j, k), matrix=None, bridge_gap=True)

def main():
  global c
  surface = cairo.PDFSurface("all-the-3x3-weave-mazes.pdf", PAGE_SIZE_PTS, PAGE_SIZE_PTS)
  c = cairo.Context(surface)
  draw_mazes()
  c.show_page()
  surface.finish()

if __name__ == "__main__":
  main()
