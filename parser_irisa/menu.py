from .transcription import Transcription #mettre un point lors du dépot gitHub
from .article import Article
from tkinter.filedialog import *
from tkinter import *
import os
import textract
"""classe du menu graphique tkinter
class Menu():

    def __init__(self):
        self.fenetre=Tk()

    def
"""


def choixSortiePDF():
    root = Tk()
    dir = askdirectory(parent = root, title='Choisissez le dossier de sortie')
    root.mainloop()
    return dir
def menu():
    """ TODO : mettre tips sélection multiple linux avec touche ctrl"""
    root = Tk()
    ent1=Entry(root,font=40)
    root.filez = askopenfilenames(initialdir = "/",title = "Sélectionnez un/des PDF(s)",filetypes=[("PDF", ".pdf"),])
    ent1.insert(END, root.filez)
    root.mainloop()
    return root.filez

if __name__=="__main__":
    rep = choixSortiePDF()
    fichiers = menu()
    print("Parsage de ce(s) pdfs : "+str(fichiers)+" dans ce dossier : "+rep+"\n")
