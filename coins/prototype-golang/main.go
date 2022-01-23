package main

import (
    "fmt"
    "github.com/anthonynsimon/bild/imgio"
    "os"
    "fowi/lab/coins-prototype/cmd"
)

func main() {
    images := os.Args[1:]
    for _, s := range images {
        fmt.Println("Processing {}", s)
        img, err := imgio.Open(s)
        if err != nil {
            fmt.Println(err)
            return
        }
        transparentBg := cmd.TransparentBackgound(img)
        if err := imgio.Save("output.png", transparentBg, imgio.PNGEncoder()); err != nil {
            fmt.Println(err)
            return
        }
    }

}
