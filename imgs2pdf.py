#!/usr/bin/env python
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

import os
from sys import argv, exit
import getopt
from PIL import Image
from reportlab.pdfgen import canvas

__VERSION__ = "3.0"
EXTENSIONES = [".jpg", ".gif", ".png", ".jpeg", ".JPG", ".GIF", ".PNG", ".JPEG"]
TITULO = os.path.split(os.getcwd())[-1]
SALIDA = "".join([TITULO, ".pdf"])
DEBUG = 0


def listaimagenes():
    """Return a list of image files from the working directory."""
    imagenes = []
    for archivo in os.listdir(os.getcwd()):
        if os.path.isfile(archivo):
            try:
                # Check whether it's a supported image format
                im = Image.open(archivo)
                # Then add it the list.
                imagenes.append(archivo)
            except IOError:
                # Or skip this file
                pass
    return sorted(imagenes)


def main():
    """Script main function."""
    global TITULO, SALIDA, DEBUG
    try:
        opcs, args = getopt.getopt(argv[1:], "cdho:t:v",
                                   ["debug", "help", "output=", "title=",
                                    "version"])
    except getopt.GetoptError:
        print(__doc__)
        exit(2)

    for opc, arg in opcs:
        if opc in ("-d", "--debug"):
            DEBUG = 1
            import sys
            import gc
        elif opc in ("-h", "--help"):
            print(__doc__)
            exit(1)
        elif opc in ("-o", "--output"):
            SALIDA = arg
        elif opc in ("-t", "--title"):
            TITULO = arg
        elif opc in ("-v", "--version"):
            print("imgs2pdf %s" % __VERSION__)
            exit(1)

    imagenes = listaimagenes()
    pdf = canvas.Canvas(SALIDA)
    pdf.setTitle(TITULO)

    for imagen in imagenes:
        print("Proccesing %s" % imagen)
        # Open the image file
        imagefile = Image.open(imagen)
        # Resize each page to fit the image size
        print("    Resizing page to %s width and %s height" % imagefile.size)
        pdf.setPageSize(imagefile.size)
        # Draw the image in the current page
        pdf.drawImage(canvas.ImageReader(imagen), 0, 0,
                      preserveAspectRatio=True)
        if DEBUG == 1:
            print(sum([sys.getsizeof(o) for o in gc.get_objects()]))
        # Close the current page and create a new one
        pdf.showPage()
    # Cerramos el PDF
    pdf.save()


if __name__ == "__main__":
    main()
