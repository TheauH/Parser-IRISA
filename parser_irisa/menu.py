from .transcription import Transcription #mettre un point lors du dépot gitHub
from .article import Article
from tkinter.filedialog import *
from tkinter import *
import os

def choixSortiePDF():
    root = Tk()
    texte = Label(root,text="Bienvenue dans PASFT, le parseur d'article scientifique PASFT\nVeuillez à choisir un répertoire et cliquer sur \"Suivant>\" pour continuer.")
    texte.pack()
    button = Button(root,text="Suivant >", command=root.destroy)
    dir = askdirectory(parent = root, title='Choisissez le dossier de sortie')
    button.pack()
    root.mainloop()
    return dir

def menu():
    root = Tk()
    ent1=Entry(root,font=40)
    texte = Label(root,text="Choisissez un ou plusieurs PDF et cliquer sur \"Suivant>\" pour finaliser l'opération.")
    texte.pack()
    button = Button(root,text="Suivant >", command=root.destroy)
    root.filez = askopenfilenames(initialdir = "/",title = "Sélectionnez un/des PDF(s)",filetypes=[("PDF", ".pdf"),])
    ent1.insert(END, root.filez)
    button.pack()
    root.mainloop()
    return root.filez

if __name__=="__main__":
    rep = choixSortiePDF()
    fichiers = menu()
    print("Parsage de ce(s) pdfs : "+str(fichiers)+" dans ce dossier : "+rep+"\n")
