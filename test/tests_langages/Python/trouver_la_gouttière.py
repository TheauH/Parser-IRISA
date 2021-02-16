from pathlib import Path
from gouttière import Gouttière
from transcription import Transcription

chemin_entrée = Path("../../Corpus_2021/Boudin-Torres-2006.pdf")
chemin_sortie = Path("sortie.txt")

# Traitement de chaque fichier P.D.F.
entrée = open(chemin_entrée, "rb")
sortie = open(chemin_sortie, 'wb')

monPDF = Transcription(entrée)
for page in monPDF:
    g = page.gouttière()
    page.append(" " * (g.get_abscisse() - 1) + "↑\n")
    for ligne in page:
        sortie.write(ligne.encode())
    print("Gouttière :", g.get_abscisse(), g.get_début(), g.get_fin())