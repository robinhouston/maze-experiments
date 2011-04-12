# Print individual 3x3 weave mazes into little PNG files

import cairo

C = 20 # cell size
B = 15 # border size
G = 6  # gap size for bridges

GAP_BETWEEN_CELLS = 40

FILL_COLOUR = (.86, .2, .2)
STROKE_COLOUR = None #(.4, .1, .1)

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

MR = cairo.Matrix(0,1, -1,0, B+C+B+C+B+C+B,0)
MB = cairo.Matrix(-1,0, 0,-1, B+C+B+C+B+C+B,B+C+B+C+B+C+B)
ML = cairo.Matrix(0,-1, 1,0, 0,B+C+B+C+B+C+B)

def maze(t, r, b, l):
  return join_branches(branch(t), branch(r, MR), branch(b, MB), branch(l, ML))

def draw_maze(*args, **kwargs):
  return draw(maze(*args, **kwargs))

def draw_branch(cell_row, cell_col, *args, **kwargs):
  with cell(cell_row, cell_col):
    b = branch(*args, **kwargs)
  draw(b)


def main(output_filename, spec_strings):
  global c
  size = B+C+B+C+B+C+B
  surface = cairo.ImageSurface(cairo.FORMAT_RGB24, size, size)
  c = cairo.Context(surface)
  
  c.rectangle(0,0, size,size)
  c.set_source_rgb(1,1,1)
  c.fill()
  
  spec = []
  for arg in spec_strings:
    if arg:
      a,b = map(int, arg.split(","))
      spec.append((a,b))
    else:
      spec.append(None)
  
  draw_maze(*spec)
  surface.write_to_png(output_filename)
  surface.finish()

if __name__ == "__main__":
  import sys
  main(sys.argv[1], sys.argv[2:])
