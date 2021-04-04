# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:52:15 2021

@author: sosob
"""
from PyPDF2 import generic
import re
from typing import Union

from .page import Première_page
from .champ import Champ
from .transcription import Transcription


def extract_information(
    pdf_text: Transcription,
    métatitre: Union[generic.TextStringObject, None] = None,
):
    page: Première_page = pdf_text[0]
    # si le titre est égale à None ou null alors vient forcer la recherche de celui ci
    if not métatitre or len(métatitre) <= 4 or métatitre.startswith("/"):
        # Récupération et concaténation des 2 premières lignes du texte
        concatenation = " ".join([ligne.strip() for ligne in page[:2]])
        # Regex pour venir rajouter un espace entre chaque majuscule de la chaine de caractère
        p = re.compile(r"([a-z])([A-Z])")
        title = re.sub(p, r"\1 \2", concatenation)
        # Le titre fait une ou deux lignes.
        titre = title
        print("pas bath")

    else:
        titre = str(métatitre)
        print("bath")

    ligne_fin = 2 if page[1].strip() in titre else 1

    # Correction, si nécessaire de la positiondébut du corps de texte
    if page.début_corps <= ligne_fin:
        vide = False
        page.début_corps = ligne_fin + 1
        for i in range(ligne_fin, len(page)):
            if not page[i]:
                if not vide:
                    vide = True
                else:
                    while not page[i]:
                        i += 1
                    page.début_corps = i
                    break

    return Champ(
        nom="titre",
        contenu=titre,
        page_début=0,
        ligne_début=0,
        page_fin=0,
        ligne_fin=ligne_fin,
    )


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
