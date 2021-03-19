import textract
import PyPDF2

# print(PyPDF2.PdfFileReader(open("test/Corpus_2021/Torres-moreno1998.pdf"), "rb"))

texte = textract.process(
    "test/Corpus_2021/Torres-moreno1998.pdf",
    method="pdftotext",
    layout=True,
    language="en",
)
sortie = open("résultat.txt", "wb")


sortie.write(texte)
