# Image To Characters Converter

Simple CLI program for converting images to images from characters (ASCII or Unicode). See examples below.

## Requirements:
* [Pillow](https://pypi.org/project/Pillow/)

## TODO:
* Add some comments
* Add custom font selection
* Bug fixes
* Add help text
* Rewrite code in another language (e.g. C++)

## Usage
```
Usage: python main.py input file [output file] [options]

Options:
-v or --verbose       enable verbose output
-c or --colored       make characters colored
-u or --unicode       use unicode characters instead of ascii 
-o or --output-txt    create text file 'output.txt' with characters

-s [float] or --scale [float]           set source image scaling (default value: 100 or one character for any pixel)
-f [integer] or --font-size [integer]   set font size (default value: 16)
-p [float] or --padding [float]         set characters padding from right and bottom (distance between characters). Default value: 0. 
                                        can take negative values
```
