"""
Maze generation algorithms.
"""

from mazer.maze import (Maze, DIRECTIONS, RELATIVE_DIRECTIONS, N, E, S, W, random_direction)
import random

def recursive_backtracking(maze):
  """Complete the maze using the recursive backtracking algorithm.
  """
  directions = [ d for d in RELATIVE_DIRECTIONS ]
  random.shuffle(directions)
  for d in maze.branch(directions):
    if maze.cell_is_empty(d):
      maze.carve(d)
      recursive_backtracking(maze)
  return maze

def kruskal(maze):
  """Complete the maze using the randomised Kruskal's algorithm.
  """
  walls = list(maze.walls())
  random.shuffle(walls)
  for x, y, d in walls:
    if not maze.is_connected(x, y, d):
      maze.carve(x, y, d)
  return maze

def aldous_broder(maze):
  """Complete the maze using the Aldous-Broder algorithm.
  (If the starting maze has no passages, then this algorithm
  will produce all possible mazes with equal probability.)
  """
  while maze.has_empty_cells():
    d = random_direction()
    if maze.cell_is_empty(d):
      maze.carve(d)
    else:
      maze.move(d)
  return maze

def _lerw(maze, c, stopping_set):
  """Perform a loop-erased random walk from starting position c
  until an element of stopping_set is hit.
  """
  path = [c]
  path_indices_by_cell = {c: [0]}
  
  maze.move(*c)
  while maze.cursor_cell() not in stopping_set:
    if maze.move(random_direction()):
      c = maze.cursor_cell()
      if c in path_indices_by_cell and path_indices_by_cell[c]:
        prev_index = path_indices_by_cell[c][-1]
        for d in path[(prev_index + 1):]:
          path_indices_by_cell[d].pop()
        path = path[:(prev_index + 1)]
      else:
        path_indices_by_cell.setdefault(c, []).append(len(path))
        path.append(c)
  
  return path

def wilson(maze):
  """Complete the maze using Wilson's algorithm.
  This will produce all possible completions with equal probability.
  """
  cells_in_maze = set([(0,0)])
  for c in maze.cells():
    if c not in cells_in_maze:
      path = _lerw(maze, c, cells_in_maze)
      maze.carve_path(path)
      cells_in_maze.update(path)
  return maze
