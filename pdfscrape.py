from PyPDF2 import PdfReader

reader = PdfReader("test.pdf")
numPages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()


print(reader)
print(numPages)
# print(page)
print(text)