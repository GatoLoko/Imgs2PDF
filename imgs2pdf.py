#!/usr/bin/env python3
# -*- coding: UTF8 -*-
#
# Copyright 2009, 2013 Raul Soriano <GatoLoko@gmail.com>
#
# Imgs2PDF is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Imgs2PDF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

"""
Usage: imgs2pdf [OPTIONS...]

  -d, --debug                  Shows debug information.
  -h, --help                   Shows this help.
  -o NAME, --output=NAME       Sets the name of the generated PDF.
  -t TITLE, --title=TITLE      Sets the PDF title.
  -v, --version                Shows imgs2pdf version.
"""

from pathlib import Path, PurePath
from contextlib import suppress
from importlib import metadata
from sys import argv, exit
import getopt
from PIL import Image
from reportlab.pdfgen import canvas

__VERSION__: str = metadata.version("imgs2pdf")
TITLE: str = PurePath(Path.cwd()).parts[-1]
OUTPUT: str = "".join([TITLE, ".pdf"])
DEBUG: bool = False


def list_image_files():
    """Return a list of image files from the working directory."""
    images_files = []
    for file in sorted(Path.cwd().iterdir()):
        if file.is_file():
            with suppress(IOError):
                # Check whether it's a supported image format
                if Image.open(file):
                    # Then add it to the list.
                    images_files.append(file)
    return sorted(images_files)


def main():
    """Script main function."""
    global TITLE, OUTPUT, DEBUG
    try:
        opcs, args = getopt.getopt(
            argv[1:],
            "cdho:t:v",
            ["debug", "help", "output=", "title=", "version"],
        )
    except getopt.GetoptError:
        print(__doc__)
        exit(2)

    for opc, arg in opcs:
        if opc in ("-d", "--debug"):
            DEBUG = True
            import sys
            import gc
        elif opc in ("-h", "--help"):
            print(__doc__)
            exit(1)
        elif opc in ("-o", "--output"):
            OUTPUT = arg
        elif opc in ("-t", "--title"):
            TITLE = arg
        elif opc in ("-v", "--version"):
            print("imgs2pdf %s" % __VERSION__)
            exit(1)

    image_files = list_image_files()
    pdf = canvas.Canvas(OUTPUT)
    pdf.setTitle(TITLE)

    for image in image_files:
        print("Proccesing %s" % image)
        # Open the image file
        imagefile = Image.open(image)
        # Resize each page to fit the image size
        print("    Resizing page to %s width and %s height" % imagefile.size)
        pdf.setPageSize(imagefile.size)
        # Draw the image in the current page
        pdf.drawImage(
            canvas.ImageReader(image), 0, 0, preserveAspectRatio=True
        )
            print(sum([sys.getsizeof(o) for o in gc.get_objects()]))
        if DEBUG:
        # Close the current page and create a new one
        pdf.showPage()
    # Save the generated PDF
    pdf.save()


if __name__ == "__main__":
    main()
