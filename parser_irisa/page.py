from genericpath import exists
from typing import List
from .gouttière import Gouttière


class Page(List[str]):
    """
    Représente une page de texte,
    composée d’une chaîne de caractères par ligne.
    """

    def __init__(self, texte: str = None):
        if texte:
            for ligne in texte.splitlines():
                self.append(ligne)
        self.a_deux_colonnes = False

    def __str__(self) -> str:
        return "\n".join(self)

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
        Trouve la gouttière séparant les deux colonnes dans une page.
        Sert à la normalisation.

        `première` : indique s’il s’agit de la première page du document,
        pour prendre en compte la présence éventuelle de blocs d’auteurs.
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
        de deux colonnes.
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

        # Gestion des colonnes de part et d’autre de la gouttière
        for x in range(début, fin + 1):
            self.colonne_gauche.append(self[x][:pos_gouttière].rstrip())
            self.colonne_droite.append(self[x][pos_gouttière:])

        self[fin + 1 :] = (
            self.colonne_droite + self[fin + 1 :]
        )  # Insertion de la colonne droite
        self[début : fin + 1] = self.colonne_gauche


class Première_page(Page):
    """
    Sous-classe pour tenir compte des particularités
    de la première page.
    """

    def trouve_début_corps(self):
        """
        Renvoie le numéro de la première ligne du corps de texte,
        après l’en-tête contenant le titre et les auteurs.
        Sert à la normalisation (découpe-page)
        """
        # Nombre de lignes non vides parcourues en tout
        non_vides = 0  # Il en faut au moins deux d’abord.
        # Nombre de lignes vides consécutives venant d’être parcourues
        lignes_vides = 0

        # Numéros de lignes vides susceptibles de marquer le début du corps
        lignes_suspectes: List[int] = []

        for numéro, ligne in enumerate(self):
            if ligne == "":
                if non_vides >= 2:
                    lignes_vides += 1
            else:
                if non_vides < 2:
                    non_vides += 1
                if lignes_vides >= 2:
                    # Si l’on vient de passer un groupe
                    # de plusieurs lignes vides, c’est suspect.
                    lignes_suspectes.append(numéro)

                    # Cas délicieux où l’on tombe
                    # sur le mot _Abstract_ en début de ligne
                    if (
                        len(ligne) >= 8
                        and ligne.lstrip()[:8] == "Abstract"
                        and numéro == lignes_suspectes[-1]
                    ):
                        return numéro

                lignes_vides = 0

        # Cas plus embêtant où l’on ne tombe pas sur le mot _Abstract_.
        # On fait le pari que la limite se trouvera vers le quart des
        # lignes suspectes trouvées au fil du texte.
        if lignes_suspectes:
            début = lignes_suspectes[len(lignes_suspectes) // 4]
        else:
            # Cas catastrophique où l’on n’a même pas trouvé une ligne suspecte.
            début = 0

        # Enfin, descente jusqu’à une ligne non vide
        while not self[début]:
            début += 1

        return début

    def gouttière(self):
        g = super().gouttière()

        # Pas de gouttière... Pas de gouttière.
        if not g:
            return g

        # On redécoupe éventuellement la gouttière en fonction
        # de la présence d’un en-tête.

        if not hasattr(self, "début_corps"):
            self.début_corps = self.trouve_début_corps()

        if self.début_corps > g.début:
            g.début = self.début_corps

        # Début du corps fixé au début de la gouttière si non déjà trouvé
        elif not self.début_corps:
            self.début_corps = g.début

        return g

    def découpe_page(self):
        """
        Fonction de normalisation de la page.
        Pour la première page,
        définit aussi le début du corps de texte.
        """
        self.début_corps = self.trouve_début_corps()
        super().découpe_page()