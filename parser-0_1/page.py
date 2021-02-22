from typing import List
from gouttière import Gouttière


class Page(List[str]):
    """
    Représente une page de texte, composée d’une chaîne de caractères par ligne.
    """

    def __init__(self, texte: str = None):
        if texte:
            for ligne in texte.splitlines():
                self.append(ligne)
        self.a_deux_colonnes = False

    def __str__(self) -> str:
        return '\n'.join(self)

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
        Trouve la gouttière séparant les deux colonnes dans une page
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
        if colonne_max_vide:
            colonne_max_vide += marge
            self.a_deux_colonnes = True
        else:
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
                début += 1
                break
            début -= 1
        while fin < len(self) - 1:
            if len(self[fin]) > colonne_max_vide and self[fin][colonne_max_vide] != " ":
                fin -= 1
                break
            fin += 1

        return Gouttière(colonne_max_vide, début, fin)  # C’est prêt

    def découpe_page(self):
        """
        Réécrit la page en tenant compte de la présence
        de deux colonnes
        """
        g = self.gouttière()
        if not g:  # Pas de gouttière, pas de découpage.
            return

        # S’il y a bel et bien deux colonnes :
        pos_gouttière = g.abscisse
        début = g.début  # Première ligne séparée
        fin = g.fin  # Dernière ligne séparée

        # Sous-pages représentant les deux colonnes
        self.colonne_gauche = Page()
        self.colonne_droite = Page()

        nouvelle_page = Page()

        # 1. Avant les colonnes
        for x in range(début):
            nouvelle_page.append(self[x])

        # 2. Gestion des colonnes
        for x in range(début, fin + 1):
            self.colonne_gauche.append(self[x][:pos_gouttière].rstrip())
            self.colonne_droite.append(self[x][pos_gouttière:])

        nouvelle_page += self.colonne_gauche + self.colonne_droite

        # 3. Après les colonnes
        for x in range(fin + 1, len(self)):
            nouvelle_page.append(self[x])

        return nouvelle_page


maPage = Page('Bonjour,\nM. Lapin.')
print(maPage)