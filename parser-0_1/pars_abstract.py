#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 12:30:22 2021

@author: Théau Huteau
"""
import os

"création fichier txt ou ecrire les résultats a partir du pdf convertit en txt"
def creationFichierResumer(f):
    str=f[0:-4]+"_resumer.txt"
    if os.path.isfile(str):
        fichier=open(str,"a")
    else:
        fichier=open(str,"w")
    return fichier
    

def rechercheMot(mot):
    pos=mot.find("Abstract")
    return mot[pos:]

    
def pars_Abstract(path):
    "fonction de parsage qui résume la partie Abstract :"
    "TODO : a optimiser par la suite"
    source=open(path,"rb")#lecture du fichier
    buf=""
    lines=source.readlines()
    source.close()
    str=b"Abstract"
    for line in lines:
        if line.find(str):
            buf=line.decode('utf-8')
            buf+="..."
            break
        
    return buf
    
        
fi="./Corpus_2021/texte/Nasr.txt"
ligne="Bonjour monsieur Abstract : "
#ab=rechercheMot(ligne)
print(pars_Abstract(fi))
#print(ab)

