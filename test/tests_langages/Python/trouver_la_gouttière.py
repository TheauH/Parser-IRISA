from pathlib import Path
from transcription import Transcription

chemin_entrées = Path("../../Corpus_2021/Boudin-Torres-2006.pdf")
chemin_sorties = Path("../../Corpus_2021/Boudin-Torres-2006.txt")

# Traitement de chaque fichier P.D.F.
entrée = open(chemin_entrées, "rb")
sortie = open(chemin_sorties / (entrée.name[:-3] + "txt"), "wb")

monPDF = Transcription(entrée)
for page in monPDF:
    g = page.gouttière()
    print("Gouttière :", g.get_abscisse(), g.get_début(), g.get_fin())