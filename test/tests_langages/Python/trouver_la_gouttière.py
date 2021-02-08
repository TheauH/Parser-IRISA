import pdftotext
from pathlib import Path

chemin_entrées = Path("../../Corpus_2021/Boudin-Torres-2006.pdf")
chemin_sorties = Path("../../Corpus_2021/Boudin-Torres-2006.txt")

# Traitement de chaque fichier P.D.F.
entrée = open(chemin_entrées, "rb")
sortie = open(chemin_sorties / (entrée.name[:-3] + "txt"), "wb")
pdf = pdftotext.PDF(entrée)  # Conversion de P.D.F. en texte brut

page = pdf[0]

colonne = largeur = longueur = 0
matrice = page.split("\n")  # Lignes : lignes ; colonnes : caractères

# Chercher la largeur maximale du document
largeur = 0
for ligne in matrice:
    if len(ligne) > largeur:
        largeur = len(ligne)


def vacuité_colonne(texte: list, abscisse: int) -> int:
    """Compte les vides dans une colonne d’un texte représenté par un tableau de lignes"""
    vides = 0
    for ligne in texte:
        if len(ligne) <= abscisse or ligne[abscisse] == " ":
            vides += 1
    return vides


# Recherche de la bonne gouttière
marge = (
    largeur // 4
)  # Largeur de la plage sur laquelle on ne recherchera pas de gouttière

# Carte donnant la vacuité de chaque colonne sur la moitié centrale du document
carte_du_vide = [vacuité_colonne(matrice, x) for x in range(marge, largeur - marge)]

# Recherche de la colonne la plus vide de l’échantillon
max_vide = (
    len(matrice) * 0.75
)  # Initialisé au seuil en-dessous duquel il n’y a qu’une colonne
colonne_max_vide = 0
for x in range(
    len(carte_du_vide) - 1, -1, -1
):  # Parcours de la carte du vide de droite à gauche
    if carte_du_vide[x] > max_vide:
        max_vide = carte_du_vide[x]
        colonne_max_vide = x


if colonne_max_vide:
    colonne_max_vide += (
        marge  # On n’oublie pas le décalage dû à la marge non recherchée
    )
    matrice.append((colonne_max_vide - 1) * " " + "↑")
else:
    matrice.append("Texte sur une seule colonne.")

page = "\n".join(matrice)
sortie.write(page.encode())