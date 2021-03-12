#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:52:15 2021
@author: sosob
"""
from PyPDF2 import PdfFileReader
import PyPDF2
import re

def extract_information(pdf_path):
    #Récupération des métadonnées 
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
    txt = f"""Titre : {information.title}"""
    #si le titre est égale à None ou null alors vient forcer la recherche de celui ci
    if len(txt) <=12 or txt.startswith("Titre : /"):
        #parcours première page du texte
        pdfFileObj = open(pdf_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0)
        txt2 = pageObj.extractText()
        #Recupération des premières lignes du texte (le titre)
        msg_splitlines = txt2.splitlines()
        headerTo = msg_splitlines[0]
        headerFrom= msg_splitlines[1]
        #Concatenation des 2 premières lignes du texte
        concatenation = headerTo +headerFrom 
        #Regex pour venir rajouter un espace entre chaque majuscule de la chaine de caractère
        p = re.compile(r'([a-z])([A-Z])')
        title = re.sub(p, r"\1 \2", concatenation)
        return "Titre : "+title
    else :
        return txt
    return information


if __name__ == '__main__':
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Boudin-Torres-2006.pdf"
    print(extract_information(path))
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Das_Martins.pdf"    
    print(extract_information(path))
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Gonzalez_2018_Wisebe.pdf"
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