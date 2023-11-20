import pdf2docx
from pdf2docx import Converter

def pdfToDocx(pdf_file, docx_file):
    print('Converting {} to {}'.format(pdf_file, docx_file))
    cv = Converter(pdf_file)
    cv.convert(docx_file)
    cv.close()


# pdf_file = '/Users/shinnk/source/pdfminer.six_open_sw/linux-3'
# docx_file = '/Users/shinnk/source/pdfminer.six_open_sw/test.docx'
# pdfToDocx(pdf_file, docx_file)


# import os
# print(os.path.dirname(__file__))