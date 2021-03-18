from config import transcription
from pathlib import Path
from os import scandir, mkdir
from shutil import rmtree

chemin_entrées = Path("test/Corpus_2021")

try:
    dossier_entrées = scandir(chemin_entrées)  # itérateur sur les fichiers de l’entrée
except NotADirectoryError:
    print("Erreur :", chemin_entrées, "n’est pas un dossier.")
    exit()

rmtree("txt", ignore_errors=True)
mkdir("txt")

for entrée in dossier_entrées:
    if entrée.name.endswith(".pdf") and entrée.is_file:
        with open(Path("txt") / (entrée.name[:-3] + "txt"), "wb") as sortie:
            t = transcription.Transcription(chemin_entrées / entrée.name)
            t.normalise()
            sortie.write(str(t).encode())