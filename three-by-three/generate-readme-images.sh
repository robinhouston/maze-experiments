#!/bin/bash

python ad-hoc-one-offs.py README_images/one-neighbour.png 0,0 "" "" ""
python ad-hoc-one-offs.py README_images/two-adjacent-neighbours.png 0,0 0,0 "" ""
python ad-hoc-one-offs.py README_images/two-opposite-neighbours.png 0,0 "" 0,0 ""
python ad-hoc-one-offs.py README_images/three-neighbours.png 0,0 0,0 "" 0,0
python ad-hoc-one-offs.py README_images/four-neighbours.png 0,0 0,0 0,0 0,0
python ad-hoc-one-offs.py README_images/weave-v.png -1,0 "" 0,0 "" R 0,0
python ad-hoc-one-offs.py README_images/weave-h.png "" 0,0 "" 0,-1 B 0,0
