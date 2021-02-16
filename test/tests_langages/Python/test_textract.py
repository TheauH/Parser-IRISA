import textract

texte = textract.process(
    "../../Corpus_2021/Boudin-Torres-2006.pdf", method="pdftotext", language="en"
)
sortie = open("résultat.txt", "wb")

sortie.write(texte)
