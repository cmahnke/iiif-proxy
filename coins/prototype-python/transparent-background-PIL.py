#!/bin/env python3

import sys, os.path
from PIL import Image, ImageDraw

seed = (1, 1)
rep_value = (0, 0, 0, 0)
thresh = 15
file = R"../data/record_DE-MUS-062622_kenom_127703/rs.jpg"

# See https://www.geeksforgeeks.org/floodfill-image-using-python-pillow/
img = Image.open(file)
img = img.convert("RGBA")

ImageDraw.floodfill(img, seed, rep_value, thresh=thresh)

img.save('output.png', "PNG")
