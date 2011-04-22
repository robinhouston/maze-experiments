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