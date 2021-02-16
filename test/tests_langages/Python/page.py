from typing import List
from gouttière import Gouttière

class Page(List[str]):
    """
    Représente une page de texte, composée d’une chaîne de caractères par ligne.
    """

    def __init__(self, texte: str):
        for ligne in texte.split("\n"):
            self.append(ligne)

    def largeur(self) -> int:
        """
        Largeur de la page,
        c’est‑à‑dire longueur de sa plus longue ligne.
        """
        l = 0
        for ligne in self:
            if len(ligne) > l:
                l = len(ligne)
        return l

    def vacuité_colonne(self, colonne: int):
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
        # 1. Recherche de l’abscisse de la gouttière
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

        # Si aucune colonne n’a été plus vide que le seuil, la recherche s’arrêti ici.
        if not colonne_max_vide:
            return None

        # 2. Recherche des ordonnées de la gouttière
        """
        Algorithme :
        On remonte le début, et on abaisse la fin, jusqu’à buter sur du texte.
        """
        début = fin = len(self) // 2
        while début:
            if (
                len(self[début]) > colonne_max_vide
                and self[début][colonne_max_vide] != " "
            ):
                print("bute sur le caractère", self[début][colonne_max_vide])
                début += 1
                break
            début -= 1
        while fin < len(self) - 1:
            if len(self[fin]) > colonne_max_vide and self[fin][colonne_max_vide] != " ":
                print("bute sur le caractère", self[fin][colonne_max_vide])
                fin -= 1
                break
            fin += 1

        return Gouttière(colonne_max_vide, début, fin)  # C’est prêt


""" Exemple
maPage = Page('Bonjour,\nM. Lapin.')
print(maPage) # ['Bonjour,', 'M. Lapin.']
"""