# -*- encoding: utf-8 -*-

class UnicodeRenderer(object):
  def __init__(self, maze):
    self.maze = maze
  
  def render(self):
    return "".join([
      self.render_row(y) + "\n"
      for y in range(self.maze.num_rows)
    ])
  
  def render_row(self, y):
    """Each cell is rendered as a 3 x 2 block of unicode characters;
    this method returns the representation of a single row of the maze,
    consisting of two lines of text separated by a LF character.
    """
    from mazer.maze import (N,E,S,W, UN,UE,US,UW)
    r = [ [None] * self.maze.num_cols for i in (0,1) ]
    for x in range(self.maze.num_cols):
      v = self.maze[x][y]
      
      r[0][x] = { 0:u"┌", N:u"│", W:u"─", N|W:u"┘", N|UW:u"┤", UN|W:u"┴" }[v & (W|UW|N|UN)] \
       + { 0:u"─", N:u" " }[v & N] \
       + { 0:u"┐", N:u"│", E:u"─", N|E:u"└", N|UE:u"├", UN|E:u"┴" }[v & (N|UN|E|UE)]
      
      r[1][x] = { 0:u"└", S:u"│", W:u"─", S|W: u"┐", S|UW: u"┤", US|W: u"┬" }[v & (W|UW|S|US)] \
       + { 0:u"─", S:u" " }[v & S] \
       + { 0:u"┘", S:u"│", E:u"─", S|E: u"┌", S|UE: u"├", US|E: u"┬" }[v & (S|US|E|UE)]
    
    return "\n".join(["".join(rr) for rr in r])


class CairoRenderer(object):
  def __init__(self, context, **options):
    self._options = {
      "fill_colour": (.86, .2, .2),
      "stroke_colour": None,
      "left": 0,
      "top": 0,
      "width": None,  # width/height override cell_width/cell_height, if set
      "height": None,
      "cell_width": 20,
      "cell_height": 20,
      "path_border_percent": 20,
      "weave_gap_percent": 5,
    }
    self.options(**options)
    
    self.context = context
  
  def options(self, **options):
    for n, v in options.items():
      if n not in self._options:
        raise ValueError("No such option '%s'" % n)
      self._options[n] = v
  
  def _width_and_height(self, maze):
    return (
      self._options["width"] or self._options["cell_width"] * maze.num_cols,
      self._options["height"] or self._options["cell_height"] * maze.num_rows,
    )
  
  def _cursor_xy(self, maze, weave_gap=False):
    from mazer.maze import (N,E,S,W)
    x, y, d = maze.cursor()
    border = self._options["path_border_percent"]
    gap = self._options["weave_gap_percent"] if weave_gap else 0
    dx, dy = {
      N: (border, 100 - border),
      E: (border, border),
      S: (100 - border, border),
      W: (100 - border, 100 - border),
    }[d]
    
    return (x * 100 + dx, y * 100 + dy)
  
  def _paths(self, maze):
    from mazer.maze import (N,E,S,W, UN,UE,US,UW, LEFT,AHEAD,RIGHT,BACK)
    
    d = {}
    
    start_cursor = (0, 0, N)
    maze.move(*start_cursor)
    
    def trace_path():
      path = []
      
      while True:
        if maze.has_exit(AHEAD):
          maze.move(AHEAD)
          path.append(self._cursor_xy(maze))
          maze.turn(LEFT)
        else:
          maze.turn(RIGHT)
          path.append(self._cursor_xy(maze))
        
        print maze.cursor()
        if maze.cursor() == start_cursor:
          break
      
      return path
    
    paths = [trace_path()]
    
    return paths
  
  def render(self, maze, **options):
    #print maze.render_as_unicode()
    import cairo
    c = self.context
    
    self.options(**options)
    
    paths = self._paths(maze)
    width, height = self._width_and_height(maze)
    ratio_x, ratio_y = 100.0 * maze.num_cols, 100.0 * maze.num_rows
    c.save()
    c.transform(cairo.Matrix(width/ratio_x, 0, 0, height/ratio_y, self._options["left"], self._options["top"]))
    
    for path in paths:
      c.move_to(*path[0])
      for point in path[1:]:
        c.line_to(*point)
      c.set_source_rgb(*self._options["fill_colour"])
      if self._options["stroke_colour"]:
        c.fill_preserve()
        c.set_source_rgb(*self._options["stroke_colour"])
        c.stroke()
      else:
        c.fill()
    
    c.restore()

