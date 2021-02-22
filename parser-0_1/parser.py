#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 16:49:47 2021

@author: theauhuteau
"""
from pars_abstract import *
from title import * 
from pars_abstract import *
from transcription import *
import sys,os

def parser(path):
    txt=Transcription(path)
    txt_resume=creationFichierResumer(txt)
    basename=os.path.basename(path)
    txt_resume.write(basename+" : "+"\n")
    txt_resume.write(extract_information(path)+"\n")
    txt_resume.write(pars_Abstract(txt)+"\n")
    txt_resume.write(auteur(path)+"\n")
    txt_resume.close()

    
arg=sys.argv[1]
if os.path.isfile(arg):
    parser(argv)
else:
    print("Erreur :fichier passer en argument, non reconnu")
    
  
    