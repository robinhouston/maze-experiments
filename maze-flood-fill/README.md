Generate animations of mazes being flood-filled. There are implementations in JavaScript for viewing in a browser (see `index.html`), and in Python for generating animated gifs (see `frames.py`).

The maze images were generated using the `make_png_maze.py` script

    ./make_png_maze.py -r 164 -c 264 -m 4 -o maze.png

It relies on the Python module `pylib-mazer`, which you will find elsewhere in this repository.
