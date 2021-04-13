import platform
from os import PathLike
from parser_irisa.page import Page, Première_page
from typing import Union, List
from os import system, remove


class Transcription(List[Page]):
    def __init__(self, chemin_source: Union[str, bytes, PathLike]):

        system('pdftotext -layout -eol unix "' + str(chemin_source) + '" tmp.txt')
        with open("tmp.txt", "r", encoding="utf-8") as résultat:
            pages_transcrites = résultat.read().split("\f")  # Résultat découpé
        remove("tmp.txt")

        self.append(Première_page(pages_transcrites[0]))
        for i in range(1, len(pages_transcrites)):
            self.append(Page(pages_transcrites[i]))

    def __str__(self) -> str:
        return "\f".join([str(page) for page in self])

    def normalise(self):
        """
        Réécrit le document pour produire un texte linéaire, exploitable directement.
        """
        for page in self:
            page.découpe_page()