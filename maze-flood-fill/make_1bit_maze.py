#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

# XXXX Only works on little-endian platforms at the moment!

import optparse

import cairo
import mazer

parser = optparse.OptionParser()
parser.add_option("-c", "--columns",
                action="store", type="int", default=100,
                help="number of columns (default %default)")
parser.add_option("-r", "--rows",
                action="store", type="int", default=100,
                help="number of rows (default %default)")
parser.add_option("-o", "--output",
                action="store", type="str",
                help="name of output file")
(options, args) = parser.parse_args()
if args:
    parser.error("Unexpected non-option argument: " + args[0])
if not options.output:
    parser.error("No output file specified")

if options.rows <= 0:
    parser.error("The maze must have at least one row")
if options.columns <= 0:
    parser.error("The maze must have at least one column")

w, h = options.columns, options.rows

maze = mazer.Maze(w, h)
mazer.generate.wilson(maze)

im = cairo.ImageSurface(cairo.FORMAT_A1, 2*w + 1, 2*h + 1)
stride = im.get_stride()
data = im.get_data()

def whiten(x, y):
    byte_index = y*stride + x//8
    data[byte_index] = chr(ord(data[byte_index]) | 0x1 << (x%8))

for y in range(h):
    for x in range(w):
        whiten(2*x+1, 2*y+1)
        v = maze[x][y]
        if v&mazer.W: whiten(2*x, 2*y+1)
        if v&mazer.E: whiten(2*x+2, 2*y+1)
        if v&mazer.N: whiten(2*x+1, 2*y)
        if v&mazer.S: whiten(2*x+1, 2*y+2)

with open(options.output, 'w') as out:
    im.write_to_png(out)
