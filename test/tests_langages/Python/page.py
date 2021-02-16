from typing import List
from gouttière import Gouttière
from trouver_la_gouttière import vacuité_colonne


class Page(List[str]):
    """
    Représente une page de texte, composée d’une chaîne de caractères par ligne.
    """

    def __init__(self, texte: str) -> None:
        for ligne in texte.split("\n"):
            self.append(ligne)

    def largeur(self) -> int:
        """
        Largeur de la page,
        c’est‑à‑dire longueur de sa plus longue ligne.
        """
        l = 0
        for ligne in self:
            if len(ligne) > largeur:
                largeur = len(ligne)
        return l

    def vacuité_colonne(self, colonne: int) -> int:
        """Nombre de vides dans une colonne de la page"""
        vides = 0
        for ligne in self:
            if len(ligne) <= colonne or ligne[colonne] == " ":
                vides += 1
        return vides

    def gouttière(self):
        """
        Trouve la gouttière séparant les deux colonnes.
        """
        largeur = self.largeur()
        # Largeur, à gauche et à droite, sur laquelle on ne cherchera pas la gouttière
        marge = largeur // 4
        # Carte donnant la vacuité de chaque colonne sur la partie centrale du document
        carte_du_vide = [self.vacuité_colonne(x) for x in range(marge, largeur - marge)]

        # Recherche de la colonne la plus vide de l’échantillon
        max_vide = (
            len(self) * 0.75
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
            return Gouttière(colonne_max_vide, 0, len(self) - 1)  # À corriger
        else:
            return None


""" Exemple
maPage = Page('Bonjour,\nM. Lapin.')
print(maPage) # ['Bonjour,', 'M. Lapin.']
"""