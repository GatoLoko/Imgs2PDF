#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
# Copyright 2009, 2010 Raul Soriano <GatoLoko@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

'''Usage: imgs2pdf [OPTIONS...]

  -d, --debug                  Shows debug information.
  -h, --help                   Shows this help.
  -o NAME, --output=NAME       Sets the name of the generated PDF.
  -t TITLE, --title=TITLE      Sets the PDF title.
  -v, --version                Shows imgs2pdf version.
'''

from __future__ import division
import os
from sys import argv, exit
import getopt
from PIL import Image
from reportlab.pdfgen import canvas

__VERSION__ = "1.2.1"
EXTENSIONES = [".jpg", ".gif", ".png", ".JPG", ".GIF", ".PNG"]
TITULO = os.path.split(os.getcwd())[-1]
SALIDA = "".join([TITULO, ".pdf"])
DEBUG = 0


def listaimagenes():
    """Return a list of image files from the working directory."""
    imagenes = []
    for archivo in os.listdir(os.getcwd()):
        if os.path.isfile(archivo):
            if os.path.splitext(archivo)[-1] in EXTENSIONES:
                imagenes.append(archivo)
    return sorted(imagenes)


def main():
    """Script main function."""
    global TITULO, SALIDA, DEBUG
    try:
        opcs, args = getopt.getopt(argv[1:], "cdho:t:v", ["debug", "help",
            "output=", "title=", "version"])
    except getopt.GetoptError:
        print(__doc__)
        exit(2)

    for opc, arg in opcs:
        if opc in ("-d", "--debug"):
            DEBUG = 1
            import sys
            import gc
            from guppy import hpy
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
            print sum([sys.getsizeof(o) for o in gc.get_objects()])
            print hpy().heap()
        # Close the current page and create a new one
        pdf.showPage()
    # Cerramos el PDF
    pdf.save()

if __name__ == "__main__":
    main()
