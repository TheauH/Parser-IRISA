from pathlib import Path
from transcription import Transcription

chemin_entrée = Path("../../Corpus_2021/Boudin-Torres-2006.pdf")
chemin_sortie = Path("résultat.txt")

# Traitement de chaque fichier P.D.F.
entrée = open(chemin_entrée, "rb")
sortie = open(chemin_sortie, 'wb')

monPDF = Transcription(entrée)
for page in monPDF:
    page = page.découpe_page()
    for ligne in page:
        sortie.write(ligne.encode())
        sortie.write(b'\n')