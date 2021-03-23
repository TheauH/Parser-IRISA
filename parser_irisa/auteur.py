# -*- coding: utf-8 -*-
from .transcription import Transcription


def auteur(trans: Transcription, fin_titre: int, début_corps: int = -1):
    page = trans[0]
    # Saut du titre :
    i = fin_titre
    while page[i] == "":  # Saute jusqu'au début des auteurs
        i += 1
    if i == 0:
        i = 1  # Les auteurs ne sont jamais sur la première ligne.

    result = []
    if début_corps == -1:
        return " ".join(page[i].split())
    while i < début_corps:
        result += " " + " ".join(page[i].split())
        i += 1
    return "".join(result)


""" Test de tout le corpus
dossier_entrées = scandir(Path("../../Corpus_2021"))
for entrée in dossier_entrées:
    if entrée.name.endswith(".pdf") and entrée.is_file:
        fichier = open(entrée, "rb")
        print("auteur : "+auteur(Transcription(fichier)))
"""

# erreur avec Iria_Juan-Manuel_Gerardo.pdf, jing-cutepaste.pdf et Torres-moreno1998.pdf
