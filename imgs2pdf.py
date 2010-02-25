#!/usr/bin/env python
# -*- coding: UTF8 -*-
#       
# Copyright 2009 GatoLoko <GatoLoko@gmail.com>
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

  -c, --compress             Enables PDF text compression
  -h, --help                 Shows this help
  -i, --inline               Use "inline" images instead of "external".
                             This can be faster, but generates bigger
                             files and may cause problems
  -o NAME, --output=NAME     Sets the name of the generated PDF 
  -r, --resize               Resize the pictures to fit in A4 page size
  -t TITLE, --title=TITLE    Sets the PDF title
  -v, --version              Shows imgs2pdf version
'''

from __future__ import division
import os
from sys import argv, exit
import getopt
from PIL import Image
from reportlab.pdfgen import canvas

__VERSION__ = "1.1"
EXTENSIONES = [ ".jpg", ".gif", ".png", ".JPG", ".GIF", ".PNG" ]
# Reportlab A4 pages have a ridiculously small resolution of 595h x 842v
ANCHOPDF = 595
ALTOPDF = 842
RESIZEA4 = False
COMPRESION = 0
INLINE = 0
TITULO = "Titulo"
SALIDA = "salida.pdf"


def redimensiona(imagen):
    """Return an scaled copy of the supplied image."""
    imagenorig = Image.open(imagen)
    ancho, alto = imagenorig.size
    if (alto / ancho) > (ALTOPDF / ANCHOPDF):
        factor = ALTOPDF / alto
    else:
        factor = ANCHOPDF / ancho
    print "A %s resizing factor will be aplied to %s" % (factor, imagen)
    # Resizing modes: NEAREST, BILINEAR, BICUBIC, ANTIALIAS
    return imagenorig.resize((int(ancho * factor), int(alto * factor)), \
            Image.NEAREST)

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
    global RESIZEA4, TITULO, SALIDA, COMPRESION, INLINE
    try:
        opcs, args = getopt.getopt(argv[1:], "chio:rt:v", ["compress", \
                "help", "inline", "output=", "resize", "title=", \
                "version"])
    except getopt.GetoptError:
        print __doc__
        exit(2)

    for opc, arg in opcs:
        if opc in ("-c", "--compress"):
            COMPRESION = 1
        elif opc in ("-h", "--help"):
            print __doc__
            exit(1)
        elif opc in ("-i", "--inline"):
            INLINE = 1
        elif opc in ("-o", "--output"):
            SALIDA = arg
        elif opc in ("-r", "--resize"):
            RESIZEA4 = True
        elif opc in ("-t", "--title"):
            TITULO = arg
        elif opc in ("-v", "--version"):
            print("imgs2pdf version %s" % __VERSION__)
            exit(1)

    imagenes = listaimagenes()
    pdf = canvas.Canvas(SALIDA)
    pdf.setTitle(TITULO)
    pdf.setPageCompression(COMPRESION)

    for imagen in imagenes:
        if RESIZEA4 is True:
            # Resize, align and print the picture in the A4 page
            print "Proccesing %s" % imagen
            # Resizing
            imagenpdf = redimensiona(imagen)
            # Calculate the page margins to center the picture
            margenhoriz = (ANCHOPDF - imagenpdf.size[0]) / 2
            margenvert = (ALTOPDF - imagenpdf.size[1]) / 2
            # Draw the picture centered in the current page
            if INLINE == 0:
                pdf.drawImage(imagenpdf, margenhoriz, margenvert, \
                        preserveAspectRatio=True)
            else:
                pdf.drawInlineImage(imagenpdf, margenhoriz, \
                        margenvert, preserveAspectRatio=True)
        else:
            # Resize each page to fit the image size
            print "Proccesing %s" % imagen
            # Open the image
            imagenorig = Image.open(imagen)
            # Resize the page
            print imagenorig.size
            pdf.setPageSize(imagenorig.size)
            # Draw the original image in the current page
            if INLINE == 0:
                pdf.drawImage(imagen, 0, 0, preserveAspectRatio=True)
            else:
                pdf.drawInlineImage(imagen, 0, 0, \
                        preserveAspectRatio=True)
        # Close the current page and create a new one
        pdf.showPage()
    # Cerramos el PDF
    pdf.save()

if __name__ == "__main__":
    main()
