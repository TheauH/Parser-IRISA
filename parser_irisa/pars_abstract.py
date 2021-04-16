#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 12:30:22 2021

@author: Théau Huteau
"""
import os

from .transcription import Transcription
from .page import Première_page
from .champ import Champ


def pars_Abstract(texte: Transcription):
    """fonction de parsage qui résume la partie Abstract :"""
    """TODO : a optimiser par la suite"""
    lines: Première_page = texte[0]  # On ne s’intéresse qu’à la première page
    ab = "Abstract"
    string = "I   "
    int1 =  r"([1-9])"
    int2 = "Introduction"
    int3 = "1. Introduction"
    page1 = 0
    page = 0
    ligne = 0
    ligne1 = 0

    for np in range(len(texte)):
        for nl in range(len(texte[np])):
            if (
                (ab in texte[np][nl])
            ):
                page = np
                ligne = nl
            if (
                (int1 in texte[np][nl])
                or (int2 in texte[np][nl])
            ):
                page1 = np       
                ligne1 = nl
            if page and page1:
                break   
   
    return Champ(
        nom="abstract",
       contenu="\n".join(texte[page][ligne : ligne1])

    )


"""création fichier txt ou ecrire les résultats a partir du pdf convertit en txt"""


def creationFichierResumer(f):
    string = f[0:-4] + "_resumer.txt"
    if os.path.isfile(string):
        fichier = open(string, "a")
    else:
        fichier = open(string, "w")
    return fichier


def rechercheMot(mot):

    pos = mot.find("Abstract")
    # return mot[pos:nl]
    return nl


if __name__ == "__main__":
    fi = "./Corpus_2021/texte/Nasr.txt"
    ligne = "Bonjour monsieur Abstract : "
    # ab=rechercheMot(ligne)
    print(pars_Abstract(fi))
    # print(ab)
