package cmd

import (
    "image"
    "image/color"
    "github.com/anthonynsimon/bild/paint"
)

func TransparentBackgound(img image.Image) *image.RGBA {
    return paint.FloodFill(img, image.Point{1, 1}, color.RGBA{0, 0, 0, 0}, 15)
}
