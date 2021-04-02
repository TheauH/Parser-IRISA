#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 12:30:22 2021

@author: Théau Huteau
"""
import os

from .transcription import Transcription
from .page import Première_page


def pars_Abstract(texte: Transcription):
    """fonction de parsage qui résume la partie Abstract :"""
    """TODO : a optimiser par la suite"""
    lines: Première_page = texte[0]  # On ne s’intéresse qu’à la première page
    # string = "Abstract"
    # buf = ""
    # for i in range(len(lines)):
    #     if string in lines[i]:
    #         buf = "\n".join(lines[i : i + 3]) + "..."
    #         break
    string = "Conclusion"
    string2 = "Result"
    string3 = "ONCLUSION"
    string4 = "Discussion"
    ligne = 0
    page = 0

    for np in range(len(texte)):
        for nl in range(len(texte[np])):    
            if ((string in texte[np][nl]) or (string2 in texte[np][nl]) or (string3 in texte[np][nl]) or (string4 in texte[np][nl]) ):
                page = np
                ligne = nl
    #si le début n'est pas trouvé, rendre vide
    if (page==0):
    	return ""

    return "\n".join(lines[lines.début_corps : lines.début_corps + 12])


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
    #return mot[pos:nl]
    return nl

if __name__ == "__main__":
    fi = "./Corpus_2021/texte/Nasr.txt"
    ligne = "Bonjour monsieur Abstract : "
    # ab=rechercheMot(ligne)
    print(pars_Abstract(fi))
    # print(ab)
