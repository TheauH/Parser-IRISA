import textract

texte = textract.process(
    "test/Corpus_2021/Boudin-Torres-2006.pdf",
    method="pdftotext",
    layout="",
    language="en",
)
sortie = open("résultat.txt", "wb")

sortie.write(texte)
