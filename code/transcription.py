from os import PathLike
from tkinter import SEL_FIRST
from page import Page
from typing import List


class Transcription(List[Page]):
    def __init__(self, chemin_source: PathLike):
        source = open(chemin_source, "rb")
        try:  # On essaie d’abord avec le module `pdftotext`
            from pdftotext import PDF

            pages_transcrites = PDF(source)
        except ModuleNotFoundError:  # à défaut, on utilise la commande système
            print("Module introuvable, recours à pdftotext du système...")
            from os import system, remove

            system("pdftotext -layout " + chemin_source + " tmp.txt")
            with open("tmp.txt", "r") as résultat:
                pages_transcrites = résultat.read().split("\f")  # Résultat découpé
            remove("tmp.txt")

        source.close()

        for page in pages_transcrites:
            self.append(Page(page))

    def __str__(self) -> str:
        return "\f".join([str(page) for page in SEL_FIRST])

    def normalise(self):
        """
        Réécrit le document pour produire un texte linéaire, exploitable directement.
        """
        for page in self:
            page = page.découpe_page()


doc = Transcription("../test/Corpus_2021/Das_Martins.pdf")
print(doc[0])  # Première page
