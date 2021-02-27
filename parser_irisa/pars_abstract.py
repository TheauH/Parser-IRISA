#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 12:30:22 2021

@author: Théau Huteau
"""
import os

from .transcription import Transcription

"création fichier txt ou ecrire les résultats a partir du pdf convertit en txt"


def creationFichierResumer(f):
    string = f[0:-4] + "_resumer.txt"
    if os.path.isfile(string):
        fichier = open(string, "a")
    else:
        fichier = open(string, "w")
    return fichier


def rechercheMot(mot):
    pos = mot.find("Abstract")
    return mot[pos:]


def pars_Abstract(texte: Transcription):
    "fonction de parsage qui résume la partie Abstract :"
    "TODO : a optimiser par la suite"
    lines = texte[0]  # On ne s’intéresse qu’à la première page
    string = "Abstract"
    buf = ""
    for i in range(len(lines)):
        if string in lines[i]:
            buf = "\n".join(lines[i : i + 3]) + "..."
            break

    return buf


if __name__ == "__main__":
    fi = "./Corpus_2021/texte/Nasr.txt"
    ligne = "Bonjour monsieur Abstract : "
    # ab=rechercheMot(ligne)
    print(pars_Abstract(fi))
    # print(ab)
