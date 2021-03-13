# -*- coding: utf-8 -*-
from .transcription import Transcription
from pathlib import Path
from os import scandir


def auteur(trans: Transcription, titre: str = "", début_corps: int=-1):
    page = trans[0]
    i = 0
    while page[i] == "":  # Saute jusqu'au début du titre
        i += 1
    # Saut du titre :
    if not titre:  # Cas où le titre n’est pas connu
        a = 0
        while page[i] != "" and a < 2:
            i += 1
            a += 1
    else:  # Cas où il l’est (à améliorer)
        while page[i].strip() in titre:
            i += 1
    while page[i] == "":  # Saute jusqu'au début des auteurs
        i += 1
    result=""
    if début_corps==-1:
        return " ".join(page[i].split())
    while i<début_corps:
        result+=" "+" ".join(page[i].split())
        i+=1
    return result


""" Test de tout le corpus
dossier_entrées = scandir(Path("../../Corpus_2021"))
for entrée in dossier_entrées:
    if entrée.name.endswith(".pdf") and entrée.is_file:
        fichier = open(entrée, "rb")
        print("auteur : "+auteur(Transcription(fichier)))
"""

# erreur avec Iria_Juan-Manuel_Gerardo.pdf, jing-cutepaste.pdf et Torres-moreno1998.pdf
