#!/bin/bash
convert $1 -liquid-rescale 50% | convert -liquid-rescale 200% | convert -modulate 50,200 | convert -emboss 0x1.1 | convert +noise Gaussian -attenuate .5 $2
