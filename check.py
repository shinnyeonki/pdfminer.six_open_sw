from pdfminer import word


pdf_file = '/Users/shinnk/source/pdfminer.six_open_sw/samples/class/linux-2.pdf'
doc_file = '/Users/shinnk/source/pdfminer.six_open_sw/test.docx'
word.pdfToDocx(pdf_file, doc_file)