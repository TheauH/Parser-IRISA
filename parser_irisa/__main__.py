from sys import argv
from pathlib import Path
from os import scandir, mkdir
from shutil import rmtree
import codecs

from .article import Article

if len(argv) < 2:
    print("Usage :", argv[0], "dossier")
    exit(1)

chemin_entrées = Path(argv[1])
chemin_sorties_txt = chemin_entrées / "txt"
chemin_sorties_xml = chemin_entrées / "xml"

try:
    dossier_entrées = scandir(chemin_entrées)  # itérateur sur les fichiers de l’entrée
except NotADirectoryError:
    print("Erreur :", chemin_entrées, " n’est pas un dossier.")
    exit()

# Suppression s’il y a lieu, et création du dossier de sortie
rmtree(chemin_sorties_txt, ignore_errors=True)
rmtree(chemin_sorties_xml, ignore_errors=True)
mkdir(chemin_sorties_txt)
mkdir(chemin_sorties_xml)

# Traitement de chaque fichier P.D.F.
for entrée in dossier_entrées:
    if entrée.name.endswith(".pdf") and entrée.is_file:
        if argv[2] == '-t':
            with open(chemin_sorties_txt / (entrée.name[:-3] + "txt"), "wb") as sortie:

                art = Article(chemin_entrées / entrée.name)

                for élément in [
                    "Nom du fichier : ",
                    art.nom,
                    "\nTitre du papier : ",
                    art.titre,
                    "\nAuteurs : ",
                    ", ".join(art.auteurs),
                    "\nRésumé : ",
                    art.résumé,
                ]:
                    sortie.write(élément.encode())
        if argv[2] == '-x':
            with open(chemin_sorties_xml / (entrée.name[:-3] + "xml"), "wb") as sortie:

                art = Article(chemin_entrées / entrée.name)
    
                for élément in [
                    "<article\n>"
                    "Nom du fichier :",
                    "<preamble>",art.nom,"</preamble>",
                    "\nTitre du papier : ",
                    "<titre>",art.titre, "</titre>",
                    "\nAuteurs : ",
                    "<auteur>",", ".join(art.auteurs),"</auteur>",
                    "\nRésumé : ",
                    "<abstract>",art.résumé,"</abstract>",
                    "</article>"
                    "\nRéférences : ",
                    "<referenes>",art.references,"</references>"
                ]:
                    sortie.write(élément.encode())
