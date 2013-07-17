#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

"""
Render frames of a flood fill animation.
"""

PIXELS_PER_FRAME = 200

import optparse
import random

import cairo


parser = optparse.OptionParser(usage="%prog [options] image")
parser.add_option("", "--out",
                action="store", type="str", default="frame%04d.png",
                help="name pattern for output files; default '%default'")
(options, args) = parser.parse_args()

if len(args) == 0:
    parser.error("No image file specified")
if len(args) > 1:
    parser.error("Unexpected argument: " + args[1])

image_filename ,= args

with open(image_filename, 'r') as f:
    im = cairo.ImageSurface.create_from_png(f)
    w, h, d = im.get_width(), im.get_height(), im.get_data()
    stride = im.get_stride()

im_cumulative = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
data_cumulative = im_cumulative.get_data()

im_this_frame = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
data_this_frame = im_this_frame.get_data()

def white(x, y):
    i = stride*y + x*4
    return (d[i:i+4] == "\xff\xff\xff\xff" and data_cumulative[i:i+4] == "\x00\x00\x00\x00")

def redden(x, y):
    i = stride*y + x*4
    data_cumulative[i:i+4] = data_this_frame[i:i+4] = "\x00\x00\xff\xff"

while True:
    x, y = map(random.randrange, (w, h))
    if white(x, y): break

queue = [(x,y)]
def do_fill():
    num_reddened = 0;
    while len(queue) > 0:
        x, y = queue.pop(0)
        if not white(x, y): continue

        while x > 0 and white(x-1, y): x -= 1
        while x < w and white(x, y):
            redden(x, y)
            if y > 0 and white(x, y-1): queue.append((x, y-1))
            if y < h-1 and white(x, y+1): queue.append((x, y+1))
            x += 1
        
            num_reddened += 1
            if num_reddened == PIXELS_PER_FRAME:
                queue[0:0] = [ (x, y) ]
                return

i = 0
while len(queue) > 0:
    do_fill()
    i += 1
    output_filename = options.out % i
    print "Writing %s..." % (output_filename,)
    with open(output_filename, 'w') as out:
        im_this_frame.write_to_png(out)
    im_this_frame = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    data_this_frame = im_this_frame.get_data()

# Can make an animated GIF using ImageMagick, e.g.
#   convert -delay 5 tumblr-maze.png $(seq -f frame%04g.png 1 404) tumblr.gif
