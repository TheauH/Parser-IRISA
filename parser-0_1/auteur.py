#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 14:20:22 2021

@author: theauhuteau
"""
from transcription import *
from pathlib import Path
from os import scandir

def auteur(trans:Transcription):
    page=trans[0]
    i=0
    while(page[i]==''): #Saute jusqu'au début du titre
        i+=1;
    a=0
    while(page[i]!='' and a<2): #Saute le titre
        i+=1
        a+=1
    while(page[i]==''): #Saute jusqu'au début des auteurs
        i+=1;
    return " ".join(page[i].split())

""" Test de tout le corpus
dossier_entrées = scandir(Path("../../Corpus_2021"))
for entrée in dossier_entrées:
    if entrée.name.endswith(".pdf") and entrée.is_file:
        fichier = open(entrée, "rb")
        print("auteur : "+auteur(Transcription(fichier)))
"""

#erreur avec Iria_Juan-Manuel_Gerardo.pdf, jing-cutepaste.pdf et Torres-moreno1998.pdf