#!/usr/bin/env python3
import os
import pdf2image
from reportlab.pdfgen import canvas  
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

def create_pdf(exam_format, output_file, exam_id=0, exam_name='', teacher_name='', show_points_possible=False):
    # Sanity check the data sent
    assert(len(exam_format) <= 90)
    for character in exam_format:
        assert(character in '.ABCDEFGH')

    OFFSETS = {
        'questions_y_top': 150,
        'questions_x_left': 66,
        'markers_y_top': 138,
        'markers_y_bottom': 30,
        'markers_x_left': 30,
        'markers_x_right': 30,
        'column_width': 178
    }
    MARKER_SIZE = (30, 30)

    exam_pdf = canvas.Canvas(output_file, pagesize=letter)
    page_width, page_height = letter

    # Create QR Code on the top right
    exam_url = 'https://bubblecheck.app/exam/{}'.format(exam_id)
    qrcode = QrCodeWidget(value=exam_url)
    qrdrawing = Drawing(width=50, height=50)
    qrdrawing.add(qrcode)
    renderPDF.draw(qrdrawing, exam_pdf, page_width-142, page_height-110)

    # Print a 'Name, Period, Date' line
    exam_pdf.drawString(50,page_height-60,'Name: ________________________      Period: ______      Date: ______')

    # Draw markers around the question area
    markers = [
        {
            'x': page_width-OFFSETS['markers_x_right']-MARKER_SIZE[0],
            'image': os.path.join('markers', 'top_right.png'), 
            'y': page_height-OFFSETS['markers_y_top']
        },
        {
            'x': OFFSETS['markers_x_right'],
            'image': os.path.join('markers', 'top_left.png'), 
            'y': page_height-OFFSETS['markers_y_top']
        },
        {
            'x': OFFSETS['markers_x_right'],
            'image': os.path.join('markers', 'bottom_left.png'), 
            'y': OFFSETS['markers_y_bottom']
        },
        {
            'x': page_width-OFFSETS['markers_x_right']-MARKER_SIZE[0],
            'image': os.path.join('markers', 'bottom_right.png'), 
            'y': OFFSETS['markers_y_bottom']
        }
    ]
    for marker in markers:
        exam_pdf.drawImage(marker['image'], marker['x'], marker['y'], width=30, height=30)

    # Print the questions
    current_column = 0 # There are three column, 0-2
    current_row = 0 # There are 25 rows, 0-24
    current_question_number = 1
    for question in exam_format:
        # Print question number
        exam_pdf.drawString(
            x=current_column*OFFSETS['column_width']+OFFSETS['questions_x_left'], 
            y=page_height-OFFSETS['questions_y_top']-(current_row*20),
            text=str(current_question_number)+'.')

        # Print question options, enclosed in circles
        if question == '.':
            characters_to_draw = ['T', 'F']
        else:
            characters_to_draw = map(chr, range(ord('A'), ord(question)+1))
        current_character_index = 0
        for character_to_draw in characters_to_draw:
            exam_pdf.setFillColor(colors.gray)
            exam_pdf.drawString(
                x=current_column*OFFSETS['column_width']+90+current_character_index*15,
                y=page_height-OFFSETS['questions_y_top']-(current_row*20),
                text=character_to_draw
            )
            exam_pdf.setFillColor(colors.black)
            exam_pdf.circle(
                x_cen = current_column*OFFSETS['column_width']+94+current_character_index*15,
                y_cen = page_height-OFFSETS['questions_y_top']+4-(current_row*20),
                r=7
            )
            current_character_index += 1

        current_row += 1
        if current_row == 30:
            current_row = 0
            current_column += 1
        current_question_number += 1

    exam_pdf.showPage()    
    exam_pdf.save()