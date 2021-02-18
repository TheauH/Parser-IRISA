# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:52:15 2021

@author: sosob
"""
from PyPDF2 import PdfFileReader
import PyPDF2

def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()

    txt = f"""Titre : {information.title}"""
    if len(txt) <=12 :
        
        pdfFileObj = open(pdf_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0)
        txt2 = pageObj.extractText()
        
        msg_splitlines = txt2.splitlines()
        headerTo = msg_splitlines[0]
        headerFrom= msg_splitlines[1]
        print("Titre : "+headerTo+headerFrom)
    else :
        print(txt)
    return information


if __name__ == '__main__':
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Boudin-Torres-2006.pdf"
    extract_information(path)
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Das_Martins.pdf"    
    extract_information(path)
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Gonzalez_2018_Wisebe.pdf"
    extract_information(path)
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Iria_Juan-Manuel_Gerardo.pdf"    
    extract_information(path)
   
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\kessler94715.pdf"    
    extract_information(path)
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\kesslerMETICS-ICDIM2019.pdf"
    extract_information(path)
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\mikheev J02-3002.pdf"    
    extract_information(path)
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Mikolov.pdf"
    extract_information(path)
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Nasr.pdf"    
    extract_information(path)
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Torres.pdf"
    extract_information(path)
    path = r"C:\Users\sosob\Desktop\S6\Projet de dev\Corpus_2021\Torres-moreno1998.pdf"    
    extract_information(path)    
    
    #text_extractor(path)
    
    
