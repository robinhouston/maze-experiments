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


import sys
sys.path.append("scripts")
import cairo, mazer, make_maze
surface = cairo.PDFSurface("/tmp/out.pdf", 6 * 72, 6 * 72)
c = cairo.Context(surface)
renderer = mazer.render.CairoRenderer(c, width=6 * 72, height=6 * 72)
m = mazer.Maze(3, 3)
make_maze.wilson(m)
renderer.render(m)
c.show_page()
surface.finish()

!open /tmp/out.pdf



import cairo, mazer
surface = cairo.PDFSurface("/tmp/weave.pdf", 3 * 72, 3 * 72)
c = cairo.Context(surface)
renderer = mazer.render.CairoRenderer(c, width=3 * 72, height=3 * 72)
m = mazer.Maze(3, 3)
m.weave(1,1,mazer.H_OVER_V)
m.move(0,1); m.carve(mazer.N); m.carve(mazer.E)
m.move(2,0); m.carve(mazer.S)
m.move(2,2); m.carve(mazer.W)
m.move(0,2); m.carve(mazer.N)
print m.render_as_unicode()
renderer.render(m)
c.show_page()
surface.finish()
