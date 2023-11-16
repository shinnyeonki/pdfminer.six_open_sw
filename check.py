from pdfminer.high_level import extract_text

text = extract_text('samples/simple1.pdf')
print(text)