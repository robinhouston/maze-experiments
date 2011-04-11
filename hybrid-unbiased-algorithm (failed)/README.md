Some code and data related to a failed attempt to devise a more efficient
algorithm for generating mazes uniformly at random, by starting with the
Aldous-Broder algorithm and then switching to Wilson's algorithm.

This project was a failure: although the hybrid algorithm *does* run faster
than either of the algorithms alone, it does not generate mazes uniformly.
The reason it doesn't work is fairly subtle, and it's one of the things I
mean to explain in the unfinished document that's in the <code>unbiased</code>
directory.

The short version is that the partial mazes generated during the execution of the two algorithms
(Aldous-Broder and Wilson's) have different and incompatible statistical properties.
A partial run of Aldous-Broder produces a tree with the property that, if you overlay it
onto a uniformly random maze, you get another uniformly random maze. By contrast, a partial
run of Wilson's algorithm produces a tree, a uniformly-chosen extension of which is a
uniformly random maze. So the hybrid algorithm has a precisely-quantifiable bias.
