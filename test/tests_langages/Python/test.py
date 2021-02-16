import pdftotext
from sys import argv
from os import scandir, mkdir
from shutil import rmtree
from pathlib import Path

def vacuité_colonne(texte: list, abscisse: int) -> int:
    """Compte les vides dans une colonne d’un texte représenté par un tableau de lignes"""
    vides = 0
    for ligne in texte:
        if len(ligne) <= abscisse or ligne[abscisse] == " ":
            vides += 1
    return vides

def trouver_la_gouttière(pdf) -> str:
    page = pdf

    largeur = 0
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
        matrice.append((colonne_max_vide - 1) * " " + "↑\n")
    else:
        matrice.append("Texte sur une seule colonne.\n")

    page = "\n".join(matrice)
    return page

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
            sortie.write(trouver_la_gouttière(page).encode())
