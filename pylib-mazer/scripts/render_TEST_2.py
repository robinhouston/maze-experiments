import cairo, mazer
surface = cairo.PDFSurface("/tmp/weave-4.pdf", 3 * 72, 3 * 72)
c = cairo.Context(surface)
renderer = mazer.render.CairoRenderer(c, width=3 * 72, height=3 * 72)
m = mazer.Maze(4, 4)
for x in (1,2):
  for y in (1,2):
    m.weave(x,y, [mazer.V_OVER_H, mazer.H_OVER_V][(x-1)*(y-1)])
m.carve(mazer.AHEAD)
m.move(0,2, mazer.S); m.carve(mazer.AHEAD); m.carve(mazer.LEFT)
m.move(2,0, mazer.E); m.carve(mazer.AHEAD); m.carve(mazer.RIGHT)
m.move(3,2, mazer.S); m.carve(mazer.AHEAD); m.carve(mazer.RIGHT)
print m.render_as_unicode()
renderer.render(m)
c.show_page()
surface.finish()
