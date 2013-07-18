#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

import optparse

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

parser.add_option("", "--column-width",
                action="store", type="int", default=3,
                help="width of one column of the maze, in pixels; default is %default")
parser.add_option("", "--width",
                action="store", type="int", default=0,
                help="width of output image (pixels)")
parser.add_option("", "--row-height",
                action="store", type="int", default=3,
                help="height of one row of the maze, in pixels; default is %default")
parser.add_option("", "--height",
                action="store", type="int", default=0,
                help="width of output image (pixels)")

parser.add_option("-m", "--margin",
                action="store", type="int", default=5,
                help="width of margin (pixels); default is %default")
(options, args) = parser.parse_args()
if args:
    parser.error("Unexpected non-option argument: " + args[0])
if not options.output:
    parser.error("No output file specified")

if options.rows <= 0:
    parser.error("The maze must have at least one row")
if options.columns <= 0:
    parser.error("The maze must have at least one column")

width = options.width
if not width:
    width = options.column_width * options.columns + 2*options.margin
if not width:
    parser.error("Neither --width nor --column-width is specified")

height = options.height
if not height:
    height = options.row_height * options.rows + 2*options.margin
if not height:
    parser.error("Neither --height nor --row-height is specified")

m = mazer.Maze(options.columns, options.rows)
mazer.generate.wilson(m)
m.render_to_png(options.output, width, height, margin=options.margin, background_colour=(0.7, 0.7, 0.7), fill_colour=(1, 1, 1), path_border_percent=100/3, draw_entrance_and_exit=False)
