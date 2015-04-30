# blood-art-to-png
Extract pictures from Monolith's Blood ART files into separate PNG.

Usage
-----
> python ./blood-art-to-png.py tilesXXX.art

Script will extract all sprites/textures into PNG (RGBA) files and will also create simple INI text file with additional informations about every one of them.

Example
-------
```
[header]
version=1
start=2048
end=2303
count=256

[tile002048.png]
index=2048
width=16
height=16
alpha=0
xoffset=0
yoffset=0
ext1=0
ext2=0

...

[tile002300.png]
index=2300
width=26
height=23
alpha=1
xoffset=3
yoffset=-1
ext1=0
ext2=0

...
```

Hopefully, header is self-explanatory. Every tile has its own section with index number, width and height in pixels, information about alpha channel (0 - image doesn't have any transparency, 1 - image has one or more transparent pixels), xoffset and yoffset (to align animated sprites) and ext1/ext2 (additional data, currently not used).

Notes
-----
Script is using [drj11/pypng](https://github.com/drj11/pypng) PNG library.

ART file specification was borrowed from **art2tga** by **Mathieu Olivier**.

Last but not least, thanks to [Ken Silverman](http://www.advsys.net/ken/) for his legendary **BUILD** engine.
