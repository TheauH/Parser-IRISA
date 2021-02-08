from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
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
    if not entrée.name.endswith("Boudin-Torres-2006.pdf") or not entrée.is_file:
        continue
    fichier = open(entrée, "rb")
    sortie = open(chemin_sorties / (entrée.name[:-3] + "txt"), "wb")

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fichier):
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        for element in layout:
            if hasattr(element, "get_text"):
                sortie.write((element.get_text() + "\n").encode())
