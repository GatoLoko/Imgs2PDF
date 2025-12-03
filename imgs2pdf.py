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

"""Imgs2PDF: converts collections of images to PDF files.

Usage: imgs2pdf [OPTIONS...]

-d, --debug                  Shows debug information.
-h, --help                   Shows this help.
-o NAME, --output=NAME       Sets the name of the generated PDF.
-t TITLE, --title=TITLE      Sets the PDF title.
-v, --version                Shows imgs2pdf version.
"""

import gc
import getopt
import sys
from contextlib import suppress
from importlib import metadata
from pathlib import Path, PurePath

from PIL import Image
from reportlab.pdfgen import canvas

__VERSION__: str = metadata.version("imgs2pdf")


class Config:
    """Config.

    Config stores variables that need to be available to multiple functions
    """

    title: str = PurePath(Path.cwd()).parts[-1]
    output: str = f"{title}.pdf"
    debug: bool = False


config = Config


def list_image_files() -> list[str]:
    """Return a list of image files from the working directory."""
    images_files: list[str] = []
    for file in sorted(Path.cwd().iterdir()):
        if file.is_file():
            with suppress(IOError):
                # Check whether it's a supported image format
                if Image.open(file):
                    # Then add it to the list.
                    images_files.append(file)
    return sorted(images_files)


def command_parse():
    try:
        opcs, _args = getopt.getopt(
            sys.argv[1:],
            "cdho:t:v",
            ["debug", "help", "output=", "title=", "version"],
        )
    except getopt.GetoptError:
        print(__doc__)
        sys.exit(2)

    for opc, arg in opcs:
        if opc in ("-d", "--debug"):
            config.debug = True
        elif opc in ("-h", "--help"):
            print(__doc__)
            sys.exit(1)
        elif opc in ("-o", "--output"):
            config.output = arg
        elif opc in ("-t", "--title"):
            config.title = arg
        elif opc in ("-v", "--version"):
            print("imgs2pdf {__VERSION__}")
            sys.exit(1)


def main() -> None:
    """Script main function."""
    command_parse()

    image_files: list[str] = list_image_files()
    if not image_files:
        print("No images found!")
        sys.exit(2)
    pdf = canvas.Canvas(filename=config.output)
    pdf.setTitle(title=config.title)

    for image in image_files:
        print("Proccesing {image}")
        # Open the image file
        imagefile = Image.open(fp=image)
        # Resize each page to fit the image size
        width, height = imagefile.size
        print(f"    Resizing page to {width} width and {height} height")
        pdf.setPageSize(imagefile.size)
        # Draw the image in the current page
        pdf.drawImage(
            image=canvas.ImageReader(fileName=image),
            x=0,
            y=0,
            preserveAspectRatio=True,
        )
        if config.debug:
            print(sum([sys.getsizeof(obj=o) for o in gc.get_objects()]))
        # Close the current page and create a new one
        pdf.showPage()
    # Save the generated PDF
    pdf.save()


if __name__ == "__main__":
    main()
