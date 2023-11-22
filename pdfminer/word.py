from pdf2docx import Converter

def pdfToDocx(pdf_file, docx_file = None):
    # 작업 폴더 위치 변경
    import os
    os.chdir('/Users/shinnk/source/pdfminer.six_open_sw')
    # python 경로 절대 경로로 변경
    pdf_file = os.path.abspath(pdf_file)
    # docx 파일이 없는 경우
    if docx_file is None:
        docx_file = pdf_file.replace('.pdf', '.docx')
    print('Converting {} to {}'.format(pdf_file, docx_file))
    cv = Converter(pdf_file)
    cv.convert(docx_file)
    cv.close()


