#!/usr/bin/env python3
import pdf2image
from reportlab.pdfgen import canvas  
from reportlab.lib.units import cm

def create_pdf(format):
    # TODO: Actually create the PDF; this is a stub
    c = canvas.Canvas('hello.pdf')
    c.drawString(9 * cm, 22 * cm, format)
    c.showPage()
    c.save()