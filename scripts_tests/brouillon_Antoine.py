import PyPDF2
from config import transcription
from pathlib import Path
from os import scandir, mkdir
from shutil import rmtree

from config import page

chemin_entrées = Path("test/Corpus_2021")

try:
    dossier_entrées = scandir(chemin_entrées)  # itérateur sur les fichiers de l’entrée
except NotADirectoryError:
    print("Erreur :", chemin_entrées, "n’est pas un dossier.")
    exit()

# rmtree("txt", ignore_errors=True)
# mkdir("txt")

# """ Corpus normalisé """
# for entrée in dossier_entrées:
#     if entrée.name.endswith(".pdf") and entrée.is_file:
#         with open(Path("txt") / (entrée.name[:-3] + "txt"), "wb") as sortie:
#             t = transcription.Transcription(chemin_entrées / entrée.name)
#             t.normalise()
#             sortie.write(str(t).encode())

# """ En-têtes du corpus"""
# with open("en-têtes.txt", "wb") as sortie:
#     for entrée in dossier_entrées:
#         if not (entrée.name.endswith(".pdf") and entrée.is_file):
#             continue
#         print(entrée.name)
#         sortie.write(b"----- " + entrée.name.encode() + b"\xc2\xa0:\n")
#         t = transcription.Transcription(chemin_entrées / entrée.name)
#         pp: page.Première_page = t[0]
#         for ligne in pp[: pp.trouve_début_corps()]:
#             sortie.write(ligne.encode())
#             sortie.write(b"\n")

""" Métadonnées du corpus """
with open("métadonnées.txt", "wb") as sortie:
    for entrée in dossier_entrées:
        if not (entrée.name.endswith(".pdf") and entrée.is_file):
            continue
        sortie.write(b"----- " + entrée.name.encode() + b"\xc2\xa0:\n")
        pdf = PyPDF2.PdfFileReader(open(chemin_entrées / entrée.name, "rb"))
        métadonnées = pdf.getDocumentInfo()
        if métadonnées.author:
            sortie.write(métadonnées.author.encode() + b"\n")
