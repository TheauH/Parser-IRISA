import pdftotext
from sys import argv
from os import scandir, mkdir
from shutil import rmtree
from pathlib import Path

if len(argv) < 2:
    print("Usage :", argv[0], "dossier")
    exit(1)

chemin_entrées = Path(argv[1])
chemin_sorties = chemin_entrées / "texte"

dossier_entrées = scandir(chemin_entrées)  # itérateur sur les fichiers de l’entrée

# Suppression s’il y a lieu, et création du dossier de sortie
rmtree(chemin_sorties, ignore_errors=True)
mkdir(chemin_sorties)

# Traitement de chaque fichier P.D.F.
for entrée in dossier_entrées:
    if entrée.name.endswith(".pdf") and entrée.is_file:
        fichier = open(entrée, "rb")
        sortie = open(chemin_sorties / (entrée.name[:-3] + "txt"), "wb")
        pdf = pdftotext.PDF(fichier) # Conversion de P.D.F. en texte brut
        for page in pdf:
            # Écriture de chaque page suivie du caractère saut de page
            sortie.write(page.encode() + b'\x0c')
