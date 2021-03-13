# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:52:15 2021

@author: sosob
"""
from os import PathLike
from PyPDF2 import PdfFileReader, generic
import re
from typing import Union

from .transcription import Transcription


def extract_information(
    pdf_path: Union[str, bytes, PathLike],
    pdf_text: Union[Transcription, None] = None,
    métatitre: Union[generic.TextStringObject, None] = None,
):
    # si le titre est égale à None ou null alors vient forcer la recherche de celui ci
    if not métatitre or len(métatitre) <= 4 or métatitre.startswith("/"):
        # Récupération de la première page, donnée ou à retrouver
        txt2 = pdf_text[0] if pdf_text else Transcription(pdf_path)[0]
        # Récupération et concaténation des 2 premières lignes du texte
        concatenation = txt2[0] + txt2[1]
        # Regex pour venir rajouter un espace entre chaque majuscule de la chaine de caractère
        p = re.compile(r"([a-z])([A-Z])")
        title = re.sub(p, r"\1 \2", concatenation)
        titre = title

    else:
        titre = métatitre

    return str(titre).strip()


if __name__ == "__main__":
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Boudin-Torres-2006.pdf"
    print(extract_information(path))
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Das_Martins.pdf"
    print(extract_information(path))
    path = (
        r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Gonzalez_2018_Wisebe.pdf"
    )
    print(extract_information(path))
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Iria_Juan-Manuel_Gerardo.pdf"
    print(extract_information(path))
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\kessler94715.pdf"
    print(extract_information(path))
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\kesslerMETICS-ICDIM2019.pdf"
    print(extract_information(path))
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\mikheev J02-3002.pdf"
    print(extract_information(path))
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Mikolov.pdf"
    print(extract_information(path))
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Nasr.pdf"
    print(extract_information(path))
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Torres.pdf"
    print(extract_information(path))
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Torres-moreno1998.pdf"
    print(extract_information(path))
