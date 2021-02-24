from sys import argv
from pathlib import Path
from os import scandir, mkdir
from shutil import rmtree

from .article import Article

if len(argv) < 2:
    print("Usage :", argv[0], "dossier")
    exit(1)

chemin_entrées = Path(argv[1])
chemin_sorties = chemin_entrées / "txt"

try:
    dossier_entrées = scandir(chemin_entrées)  # itérateur sur les fichiers de l’entrée
except NotADirectoryError:
    print("Erreur :", chemin_entrées, " n’est pas un dossier.")
    exit()

# Suppression s’il y a lieu, et création du dossier de sortie
rmtree(chemin_sorties, ignore_errors=True)
mkdir(chemin_sorties)

# Traitement de chaque fichier P.D.F.
for entrée in dossier_entrées:
    if entrée.name.endswith(".pdf") and entrée.is_file:
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
            ]:
                sortie.write(élément.encode())
