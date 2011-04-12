There are exactly 256 different 3×3 weave mazes, which is an amusing little coincidence.
The script <code>periodic-table-of-3x3.py</code> generates a PDF file laying them all out
on a 16x16 grid.

# Classification of 3×3 weave mazes

The three-by-three grid is simple enough that the mazes can be classified by hand.
Ignoring weaves for the moment (so just considering ordinary perfect mazes), I grouped
the mazes according to the neighbours of the central cell, as follows.

## One neighbour

![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/one-neighbour.png)

There are eight of these, in each of four orientations, for a total of <b>32 mazes</b> of this type.

## Two adjacent neighbours

![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/two-adjacent-neighbours.png)

There are 2 × 6 = 12 of these, in each of four orientations, for a total of <b>48 mazes</b> of this type.

## Two opposite neighbours

![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/two-opposite-neighbours.png)

There are 4 × 4 = 16 of these, in each of two orientations, for a total of <b>32 mazes</b> of this type.

## Three neighbours

![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/three-neighbours.png)

There are 2 × 2 × 4 = 16 of these, in each of four orientations, for a total of <b>64 mazes</b> of this type.

## Four neighbours

![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/four-neighbours.png)

Each corner cell can be attached to either one of its two neighbours,
so there are a total of 2<sup>4</sup> = <b>16 mazes</b> of this type.

## Woven mazes

There is only one possible location for a weave in a 3×3 maze: in the middle. The two branches of
the weave must meet at one of the four corners. So there are two possibilities for the weave, up
to rotational symmetry:

![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/weave-v.png)
![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/weave-h.png)

Each of the three remaining corner cells can be attached to either one of its two neighbours,
so there are 2 × 2<sup>3</sup> = 16 woven mazes, in each of four orientations,
for a total of <b>64 mazes</b> of this type.
