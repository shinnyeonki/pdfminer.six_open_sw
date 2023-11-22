from pdfminer import word


pdf_file = 'samples/class/linux-2.pdf' # 바꾸고 싶은 pdf 파일 경로
doc_file = 'test.docx' # 바꿀 파일 이름 및 경로 따로 지정하지 않아도 동작함
word.pdfToDocx(pdf_file, doc_file)