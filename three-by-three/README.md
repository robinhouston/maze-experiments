There are exactly 256 different 3x3 weave mazes, which is an amusing little coincidence.
The script <code>periodic-table-of-3x3.py</code> generates a PDF file laying them all out
on a 16x16 grid.

# Classification of 3x3 weave mazes

The three-by-three grid is simple enough that the mazes can be classified by hand.
Ignoring weaves for the moment (so just considering ordinary perfect mazes), I grouped
the mazes according to the neighbours of the central cell, as follows.

## One neighbour

![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/one-neighbour.png)

## Two adjacent neighbours

![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/two-adjacent-neighbours.png)

## Two opposite neighbours

![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/two-opposite-neighbours.png)

## Three neighbours

![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/three-neighbours.png)

This pattern has four possible orientations.
For each orientation:
* each of the two isolated corners (at the top in the picture here)
  can be attached to either one of its neighbours, for a total of
  2<sup>2</sup> = 4 possibilities;
* there are four ways to fill out the bottom part

## Four neighbours

![](/robinhouston/maze-experiments/raw/master/three-by-three/README_images/four-neighbours.png)

Each corner cell can be attached to either one of its two neighbours,
so there are a total of 2<sup>4</sup> = <b>16 mazes</b> of this type.

## Woven mazes