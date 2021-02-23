import PyPDF2

pdf = PyPDF2.PdfFileReader(open("test/Corpus_2021/Boudin-Torres-2006.pdf", "rb"))

print(pdf.getPage(2).extractText())