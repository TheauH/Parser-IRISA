from sys import argv
from pathlib import Path
from os import scandir, mkdir
from shutil import rmtree
import codecs

from .article import Article

if len(argv) < 3:
    print("Usage :", argv[0], "dossier (-t|-x)")
    """TODO Meilleure doc (trouver un module dédié ?)"""
    exit(1)

if not argv[2] in ("-t", "-x"):
    print("Erreur : format incorrect.\nFormats acceptés : -t (texte) ; -x (xml)")
    exit(1)

demandeXML = argv[2] == "-x"  # Si l’utilisateur demande une sortie en X.M.L.

chemin_entrées = Path(argv[1])
chemin_sorties = chemin_entrées / ("xml" if demandeXML else "txt")

try:
    dossier_entrées = scandir(chemin_entrées)  # itérateur sur les fichiers de l’entrée
except NotADirectoryError:
    print("Erreur :", chemin_entrées, "n’est pas un dossier.")
    exit()

# Suppression s’il y a lieu, et création du dossier de sortie

rmtree(chemin_sorties, ignore_errors=True)
mkdir(chemin_sorties)

# Traitement de chaque fichier P.D.F.
for entrée in dossier_entrées:
    if entrée.name.endswith(".pdf") and entrée.is_file:
        if demandeXML: # Si demande une sortie en X.M.L.
            with open(chemin_sorties / (entrée.name[:-3] + "xml"), "wb") as sortie:

                art = Article(chemin_entrées / entrée.name)

                for élément in [
                    "<article>",
                    "<preamble>",
                    art.nom,
                    "</preamble>",
                    "<titre>",
                    art.titre,
                    "</titre>",
                    "<auteur>",
                    ", ".join(art.auteurs),
                    "</auteur>",
                    "<abstract>",
                    art.résumé,
                    "</abstract>",
                    "<Conclusion>",
                    art.conclusion,
                    "</conclusion>",
                    "<discussion>",
                    art.discussion,
                    "</discussion>",
                    "<biblio>",
                    art.references,
                    "</biblio>",
                    "</article>",

                ]:
                    sortie.write(élément.encode() + b"\n")

        else: # Si demande une sortie en texte
            with open(chemin_sorties / (entrée.name[:-3] + "txt"), "wb") as sortie:

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
                    "\nConclusion : ",
                    art.conclusion,
                    "\nDiscussion : ",
                    art.discussion,
                    "\nRéférences : ",
                    art.references,

                ]:
                    sortie.write(élément.encode())
