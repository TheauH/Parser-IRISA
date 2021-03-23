# -*- coding: utf-8 -*-
from PyPDF2 import generic
from typing import Union

from .champ import Champ
from .transcription import Transcription


def auteur(
    trans: Transcription,
    métaauteurs: Union[generic.TextStringObject, None] = None,
    fin_titre: int = 2,
    début_corps: int = -1,
):
    page = trans[0]
    # Saut du titre :
    i = fin_titre
    while page[i] == "":  # Saute jusqu'au début des auteurs
        i += 1
    if i == 0:
        i = 1  # Les auteurs ne sont jamais sur la première ligne.
    début_bloc = i

    result = []
    if début_corps == -1:
        result.append(" ".join(page[i].split()))
    fin_bloc = i + 1
    while i < début_corps:
        if not page[i]:
            i += 1
            continue
        result += " " + " ".join(page[i].split())
        i += 1
        fin_bloc = i
    result = ["".join(result)]

    return Champ(result, 0, début_bloc, 0, fin_bloc)


""" Test de tout le corpus
dossier_entrées = scandir(Path("../../Corpus_2021"))
for entrée in dossier_entrées:
    if entrée.name.endswith(".pdf") and entrée.is_file:
        fichier = open(entrée, "rb")
        print("auteur : "+auteur(Transcription(fichier)))
"""

# erreur avec Iria_Juan-Manuel_Gerardo.pdf, jing-cutepaste.pdf et Torres-moreno1998.pdf
