# Some little bits of test code for copy-pasting into ipython

import mazer
m = mazer.Maze(10, 10)
m.weave(3, 3, mazer.H_OVER_V)
m.weave(4, 4, mazer.V_OVER_H)
m.weave(5, 5, mazer.H_OVER_V)
print m.render_as_unicode()



import mazer, sys
sys.path.append("scripts")
import make_maze
m = mazer.Maze(10,10)
m.weave(4, 4, mazer.V_OVER_H)
make_maze.kruskal(m)
print m.render_as_unicode()



import mazer, sys
sys.path.append("scripts")
import make_maze
m = mazer.Maze(10,10)
make_maze.aldous_broder(m)
print m.render_as_unicode()



import mazer, sys
sys.path.append("scripts")
import make_maze
m = mazer.Maze(50,100)
make_maze.wilson(m)
print m.render_as_unicode()



import mazer
m = mazer.Maze(10, 10)
m.weave(4, 4, mazer.V_OVER_H)
m.weave(5, 4, mazer.H_OVER_V)
print m.render_as_unicode()
