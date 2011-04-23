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
  
  def _cursor_xy(self, maze, gap_x=0, gap_y=0):
    from mazer.maze import (N,E,S,W)
    x, y, d = maze.cursor()
    border = self._options["path_border_percent"]
    
    dx, dy = {
      N: (border - gap_x, 100 - border + gap_y),
      E: (border - gap_y, border - gap_x),
      S: (100 - border + gap_x, border - gap_y),
      W: (100 - border + gap_y, 100 - border + gap_x),
    }[d]
    
    return (x * 100 + dx, y * 100 + dy)
  
  def _paths(self, maze):
    from mazer.maze import (N,E,S,W, UN,UE,US,UW, LEFT,AHEAD,RIGHT,BACK)
    wg = self._options["weave_gap_percent"]
    
    def trace_path(start_cursor, other_components, already_seen, under=False):
      print "trace_path(%s)" % (start_cursor,)
      
      path = []
      maze.move(*start_cursor)
      if under:
        maze.move(AHEAD)
        start_cursor = maze.cursor()
        
        if maze.underpiece(BACK):
          if maze.cursor() not in already_seen:
            other_components.append(maze.cursor())
          path.append(self._cursor_xy(maze, 0,wg))
          maze.turn(LEFT)
          path.append(self._cursor_xy(maze, wg,0))
          maze.turn(LEFT)
          already_seen.add(maze.cursor())
          maze.move(AHEAD)
          path.append(self._cursor_xy(maze, 0,wg))
          maze.turn(LEFT)
          path.append(self._cursor_xy(maze, wg,0))
          
          return path
      
      while True:
        if maze.has_exit(AHEAD):
          maze.move(AHEAD)
          path.append(self._cursor_xy(maze))
          maze.turn(LEFT)
        else:
          if maze.has_exit(AHEAD, under=True):
            maze.move(AHEAD)
            path.append(self._cursor_xy(maze, 0,wg))
            if maze.cursor() not in already_seen:
              other_components.append(maze.cursor())
            maze.turn(LEFT)
            path.append(self._cursor_xy(maze, wg,0))
            maze.turn(LEFT)
            already_seen.add(maze.cursor())
            maze.move(AHEAD)
            path.append(self._cursor_xy(maze))
            maze.turn(BACK)
          
          maze.turn(RIGHT)
          path.append(self._cursor_xy(maze))
        
        if maze.cursor() == start_cursor:
          break
      
      return path
    
    other_components, already_seen = [], set()
    paths = [ trace_path( (0, 0, N), other_components, already_seen ) ]
    while other_components:
      component = other_components.pop(0)
      print component, already_seen
      paths.append(trace_path(component, other_components, already_seen, under=True))
      
    return paths
  
  def render(self, maze, **options):
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
