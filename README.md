# Readme

## What is Imgs2PDF

Imgs2PDF is a tool that makes PDF files from collections of independent
image files.

## Why I started Imgs2PDF instead of using ImageMagic's convert?

At the time I started Imgs2PDF, convert had a bug that made it use LOTS
of RAM.

I hit it when doing a "convert *.jpg output.pdf" on a folder with a
total of ~50MB and files between 150-500KB. I didn't know about this
problem, so I launched it and started doing something else, until I
noticed the computer becoming slow and unresponsive.

Looking for the cause, I found convert using over 3.5GB of memory on a
system with just 2GB of RAM, that means it was using 1.5GB of SWAP...
And kept growing!

For some reason, convert was opening each file, converting them to
bitmap, and storing all those bitmaps in RAM before even trying to
start writing the output PDF. A 640x480 with 32bit color image in JPEG
format may take around 40-50KB, the same image in bitmap format takes
1200KB. That's 26,6 times more!

A quick (inaccurate) calculation gives that my ~50MB of image would take
around 1330MB as bitmaps, but convert was using more than two times
that!

So I made a quick and hackish script to do the same conversion and see
if there was any difference, and my script did the work using less than
100MB of RAM and A LOT FASTER!

## Relative performance

Since ImageMagic's convert is a compiled binary program written in C,
the sane thing would be to think it is a lot faster than Imgs2PDF's
interpreted code, but in my tests they are mostly the same thing, and
most times Imgs2PDF is faster.

To test this, I have used a sample folder with 167 files, mixing JPEG
and PNG files ranging from 43KB up to 2,1MB for a combined size of
113MB. The commands used are "time convert * convert.pdf" and "time
imgs2pdf -o imgs2pdf.pdf". This way both of them will look and convert
every file, and have a given name for the output instead of choosing by
themselves.

  Command  |  Real   |  User   |   Sys   |  PDF size  | PDF Version
 :--------:|:-------:|:-------:|:-------:|:----------:|:-----------:
  convert  | 36.857s | 23.405s | 03.296s | 122743140B |     1.3
  imgs2pdf | 21.816s | 15.333s | 01.256s | 151316617B |     1.3


So, surprisingly, Imgs2PDF is actually faster than convert, but outputs
bigger files.

## Output quality

ImageMagic's generated PDFs are smaller because it converts non JPEG
files to JPEG.

Even with digital formats, any conversion involves some kind of quality
loss, so even in the best case, ImageMagic is losing some quality for
each non JPEG file.

What's more, some formats like PNGs are usually larger than JPEG
because they use a lossless compression, while JPEG uses a lossy
compression. In this cases, ImageMagic may be losing a lot of image
quality for a single PNG file. Imagine a diagram or technical drawing
with lines as thin as a single pixel. While PNG stores a flawless copy
of that diagram, JPEG isn't mean for those cases, and even at it's best
quality would store an incomplete, and may be invalid, copy of the
image.

Imgs2PDF uses PDF Image Xobjects (supported at least since PDF 1.2) to
store non JPEG files. In this PNG case, it stores a copy of the actual
PNG file, without altering it in any form, thus producing a bigger
size, but at the same time higher quality output.

## Summarizing

Imgs2PDF is faster, even when generating better quality PDFs
