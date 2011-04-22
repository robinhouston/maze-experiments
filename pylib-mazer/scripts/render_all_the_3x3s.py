import cairo, mazer

PAGE_SIZE_PTS = 6 * 72
FILL_COLOUR = (.86, .2, .2)


def render_mazes(renderer):
  

def main(output_filename):
  surface = cairo.PDFSurface(output_filename, PAGE_SIZE_PTS, PAGE_SIZE_PTS)
  c = cairo.Context(surface)
  renderer = mazer.render.CairoRenderer(c,
    fill_colour = (.86, .2, .2),
    
  )
  render_mazes(renderer)
  c.show_page()
  surface.finish()

if __name__ == "__main__":
  import sys
  main(sys.argv[1])
