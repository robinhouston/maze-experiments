import cairo, mazer
from mazer import (N, E, S, W, LEFT, AHEAD, RIGHT)

PAGE_SIZE = 6 * 72
FILL_COLOUR = (.86, .2, .2)

PAGE_MARGIN = 36.0
BLOCK_MARGIN = 1.5

BLOCK_SIZE = (PAGE_SIZE - 2 * PAGE_MARGIN) / 16

def maze(*arms):
  m = mazer.Maze(3,3)
  for direction, arm in zip([N,E,S,W], arms):
    if arm:
      m.move(1, 1, direction)
      m.carve(AHEAD)
      arm_d = dict(zip([LEFT, RIGHT], arm))
      for d in m.branch([LEFT, RIGHT]):
        for i in range(arm_d[d]):
          m.carve(AHEAD) or m.carve(d)
  return m

def render_mazes(renderer):
  def draw_maze(y, x, arms):
    m = maze(*arms)
    renderer.render(m,
      left = PAGE_MARGIN + x * BLOCK_SIZE + BLOCK_MARGIN,
      top = PAGE_MARGIN + y * BLOCK_SIZE + BLOCK_MARGIN,
      width = BLOCK_SIZE - 2 * BLOCK_MARGIN,
      height = BLOCK_SIZE - 2 * BLOCK_MARGIN,
    )
  
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

def main(output_filename):
  surface = cairo.PDFSurface(output_filename, PAGE_SIZE, PAGE_SIZE)
  c = cairo.Context(surface)
  renderer = mazer.render.CairoRenderer(c)
  render_mazes(renderer)
  c.show_page()
  surface.finish()

if __name__ == "__main__":
  import sys
  main(sys.argv[1])
