from os import PathLike
from parser_irisa.page import Page
from typing import Union, List


class Transcription(List[Page]):
    def __init__(self, chemin_source: Union[str, bytes, PathLike]):
        source = open(chemin_source, "rb")
        try:  # On essaie d’abord avec le module `pdftotext`
            from pdftotext import PDF

            pages_transcrites = PDF(source)

        except ModuleNotFoundError:  # à défaut, on utilise la commande système
            print("Module introuvable, recours à pdftotext du système...")
            from os import system, remove

            system("pdftotext -layout " + str(chemin_source) + " tmp.txt")
            with open("tmp.txt", "r") as résultat:
                pages_transcrites = résultat.read().split("\f")  # Résultat découpé
            remove("tmp.txt")

        source.close()

        for page in pages_transcrites:
            self.append(Page(page))

    def __str__(self) -> str:
        return "\f".join([str(page) for page in self])

    def normalise(self):
        """
        Réécrit le document pour produire un texte linéaire, exploitable directement.
        """
        for page in self:
            page.découpe_page()