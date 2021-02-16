from pdftotext import PDF
from io import BufferedReader
from page import Page
from typing import List

class Transcription(List[Page]):
    def __init__(self, fichier_PDF: BufferedReader):
        for page in PDF(fichier_PDF):
            self.append(Page(page))

""" Exemple (long)
fichier = open('../../Corpus_2021/Das_Martins.pdf', 'rb')
doc = Transcription(fichier)
print(doc)
"""